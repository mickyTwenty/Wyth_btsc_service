import aiohttp

class MappingUtils:
    G_MATRIX_API_BASE_URL='https://maps.googleapis.com/maps/api/distancematrix/json'
    G_API_KEY = 'AIzaSyAN0K4Ei4-P4xQpom0riNK2V5Elc7GQNk0'
    METERS_TO_MILES = 0.000621371

    def get_distance_by_city(source_city: str, destination_city: str):
        return 135

    async def get_distance_by_place_id(src_place_id: str, dst_place_id: str):
        '''uses google matrix api to distance and time estimates for a trip by place_id'''
        params = {'key': MappingUtils.G_API_KEY,
                  'origins': 'place_id:{}'.format(src_place_id),
                  'destinations': 'place_id:{}'.format(dst_place_id),
                  'mode': 'driving',
                  'units': 'imperial'}
        async with aiohttp.ClientSession() as session:
            async with session.get(url=MappingUtils.G_MATRIX_API_BASE_URL, params = params) as resp:
                r_json = await resp.json()
                duration_sec = int(r_json['rows'][0]['elements'][0]['duration']['value'])
                distance_meters = int(r_json['rows'][0]['elements'][0]['distance']['value'])

                return {'miles': distance_meters * MappingUtils.METERS_TO_MILES,
                        'distance_txt': r_json['rows'][0]['elements'][0]['distance']['text'],
                        'minutes': duration_sec / 60,
                        'duration_txt': r_json['rows'][0]['elements'][0]['duration']['text']}



    def get_city_for_campus(campus: str):
        return 'Romeovile'

