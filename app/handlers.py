import json
from aiohttp import web
from db.data_store import BTS_DataStore
from mapping_utils import MappingUtils
from fare_utils import FareUtils
import asyncio


class Handlers:
    def __init__(self):
        self._bts_datastore = BTS_DataStore()

    async def get_total_co2_handler(self, request):
        bts_datastore = BTS_DataStore()

        response = await bts_datastore.get_totals()
        del response['total_donations']
        return web.json_response(response)


    async def get_total_charity_handler(self, request):
        bts_datastore = BTS_DataStore()

        response = await bts_datastore.get_totals()
        del response['total_co2_emissions']
        return web.json_response(response)

    async def get_totals(self, request):
        extended = request.query.get('extended')
        bts_datastore = BTS_DataStore()

        response = await bts_datastore.get_totals()

        if extended and extended == '1':
            seats_offered = await bts_datastore.get_total_seats_offered()
            seats_demanded = await bts_datastore.get_total_seats_demanded()
            n_participants = await bts_datastore.get_participating_colleges()
            schools_by_co2 = await bts_datastore.get_co2_award()
            schools_by_donation = await bts_datastore.get_donation_award()


            response.update(seats_offered)
            response.update(seats_demanded)
            response.update(n_participants)
            response.update({"schools_by_co2": schools_by_co2})
            response.update({"schools_by_donation": schools_by_donation})

        return web.json_response(response)



    async def trip_estimates_handler(self, request, driver_mode = True):
        src_place_id = request.query['src_place_id']
        dst_place_id = request.query['dst_place_id']

        rider_payload = await request.json()

        raw_src = rider_payload['src_raw_auto_complete']
        raw_dst = rider_payload['dst_raw_auto_complete']

        src_city = raw_src['description']
        dst_campus = raw_dst['description']

        seats = int(request.query['seats']) if driver_mode else 1
        donation = (float(request.query['donation']) or 1) if driver_mode else float(request.query['donation'])
        trip_payload = await request.json()

        trip_estimates = await MappingUtils.get_distance_by_place_id(src_place_id = src_place_id, dst_place_id = dst_place_id)
        co2 = FareUtils.get_co2_by_miles(miles = trip_estimates['miles'], seats = seats)


        response = {"co2_savings": int(co2),
                    "trip_miles": int(trip_estimates['miles']),
                    "trip_duration_min": int(trip_estimates['minutes'])
                    }

        if driver_mode:
            trip_financials = FareUtils.get_fare_split(miles=trip_estimates['miles'],
                                                donation_percentage=donation,
                                                seats=seats)

            response.update({"driver_earnings": trip_financials['driver']})
            response.update({"donation": round(trip_financials['donation'], 2)})

            asyncio.get_event_loop().create_task(self._bts_datastore.store_ride_estimate({
                                              "home_city": src_city,
                                              "campus": dst_campus,
                                              "available_seats": seats,
                                              "total_miles": trip_estimates['miles'],
                                              "co2_emissions": int(co2),
                                              "driver_fare": trip_financials['driver'],
                                              "donation": trip_financials['donation'],
                                              "wyth_fare": trip_financials['wyth'],
                                              "src_raw_place": raw_src,
                                              "dst_raw_place": raw_dst}))

        else:
            offer = FareUtils.get_offer_estimate(miles=trip_estimates['miles'], donation=donation)
            response.update({"rider_offer": offer['offer_estimate']})
            response.update({"donation": round(offer['donation'], 2)})

            asyncio.get_event_loop().create_task(self._bts_datastore.store_ride_request_estimate({
                                              "home_city": src_city,
                                              "campus": dst_campus,
                                              "total_miles": trip_estimates['miles'],
                                              "co2_emissions": int(co2),
                                              "rider_offer": offer['offer_estimate'],
                                              "donation": offer['donation'],
                                              "src_raw_place": raw_src,
                                              "dst_raw_place": raw_dst}))

        return web.json_response(response)

    async def post_new_ride_handler(self, request):
        rider_payload = await request.json()

        raw_src = rider_payload['src_raw_auto_complete']
        raw_dst = rider_payload['dst_raw_auto_complete']
        src_city = raw_src['description']
        dst_campus = raw_dst['description']


        src_place_id = rider_payload['src_place_id']
        dst_place_id = rider_payload['dst_place_id']

        seats_offered = rider_payload.get('seats') or 1

        donation_percentage = rider_payload['donation']

        trip_miles = await MappingUtils.get_distance_by_place_id(src_place_id = src_place_id, dst_place_id = dst_place_id)
        trip_miles = trip_miles['miles']

        co2_emissions = FareUtils.get_co2_by_miles(trip_miles, seats_offered)

        fare_split = FareUtils.get_fare_split(miles= trip_miles,
                                              donation_percentage = donation_percentage,
                                              seats = seats_offered)

        await self._bts_datastore.store_a_ride({"driver_name": rider_payload['name'],
                                                "email": rider_payload['email'],
                                                "home_city": src_city,
                                                "campus": dst_campus,
                                                "available_seats": rider_payload['seats'],
                                                "total_miles": trip_miles,
                                                "co2_emissions": co2_emissions,
                                                "driver_fare": fare_split['driver'],
                                                "donation": fare_split['donation'],
                                                "wyth_fare": fare_split['wyth'],
                                                "src_raw_place": rider_payload['src_raw_auto_complete'],
                                                "dst_raw_place": rider_payload['src_raw_auto_complete']})

        return web.json_response({"code": 200,
                                  "message": "ride is created successfully",
                                  "contribution": {
                                      "co2_saved": co2_emissions,
                                      "charity": fare_split['donation'],
                                      "driver_share": fare_split['driver'],
                                      "wyth_share": fare_split['wyth']
                                  }
                                  }
                                 )

    async def post_new_rider_trip_handler(self, request):
        rider_payload = await request.json()

        raw_src = rider_payload['src_raw_auto_complete']
        raw_dst = rider_payload['dst_raw_auto_complete']
        src_city = raw_src['description']
        dst_campus = raw_dst['description']


        src_place_id = rider_payload['src_place_id']
        dst_place_id = rider_payload['dst_place_id']

        donation_amount = rider_payload['donation']

        trip_miles = await MappingUtils.get_distance_by_place_id(src_place_id = src_place_id, dst_place_id = dst_place_id)
        trip_miles = trip_miles['miles']

        co2_emissions = FareUtils.get_co2_by_miles(trip_miles)

        rider_offer = FareUtils.get_offer_estimate(miles= trip_miles,
                                                  donation = donation_amount)


        await self._bts_datastore.store_a_rider_ride(
                {
                    "rider_name": rider_payload['name'],
                    "email": rider_payload['email'],
                    "home_city": src_city,
                    "campus": dst_campus,
                    "total_miles": trip_miles,
                    "co2_emissions": co2_emissions,
                    "rider_offer": rider_offer['offer_estimate'],
                    "donation": rider_offer['donation'],
                    "src_raw_place": raw_src,
                    "dst_raw_place": raw_dst
                }
        )

        return web.json_response({"code": 200,
                                  "message": "ride request is created successfully",
                                  "contribution": {
                                      "co2_saved": co2_emissions,
                                      "charity": rider_offer['donation'],
                                      "offer":rider_offer['offer_estimate']
                                  }}
                                 )

    async def contact_us_handler(self, request):
        payload = await request.json()
        try:
            await self._bts_datastore.store_contact_us(payload)

            return web.json_response({"message": "Thank you for contacting us, someone will reach out to you soon."})

        except:
            return web.json_response({"message": "Something went wrong, please, resubmit your message"})
