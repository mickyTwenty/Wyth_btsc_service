class FareUtils:
    CO2_PER_MILE = 1
    FARE_PER_MILE = 20 # in cents range 20, 25 cents.
    FARE_PER_MILE_HIGH = 25
    WYTH_FEE_PERCENTAGE = 0.25

    def get_high_from_low(low_estimate):
        high = low_estimate * (1 + (FareUtils.FARE_PER_MILE_HIGH - FareUtils.FARE_PER_MILE) / FareUtils.FARE_PER_MILE)
        return round(high, 2)

    def get_co2_by_miles(miles: int, seats: int = 1):
        '''finds and returns co2 emissions in lbs'''
        return miles * FareUtils.CO2_PER_MILE * seats

    def get_offer_estimate(miles: int,
                           donation: int):
        offer_estimate = round(miles * FareUtils.FARE_PER_MILE / 100, 2)

        return {"offer_estimate": {"low": offer_estimate,
                                   "high": FareUtils.get_high_from_low(offer_estimate)},
                "donation": donation}


    def get_fare_split(miles: int, donation_percentage: float, seats: int):
        '''donation should come out of the cross.'''
        trip_total = miles * FareUtils.FARE_PER_MILE / 100 * seats

        donation_amount = trip_total * donation_percentage
        wyth_portion = (trip_total - donation_amount) * FareUtils.WYTH_FEE_PERCENTAGE
        driver_amount = trip_total - donation_amount - wyth_portion

        driver_low = round(driver_amount, 2)
        driver_high = FareUtils.get_high_from_low(driver_low)
        driver_high = round(driver_high, 2)

        return {"driver": {"low": driver_low,
                           "high": driver_high},
                "donation": donation_amount,
                "wyth": wyth_portion}