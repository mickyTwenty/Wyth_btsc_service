from datetime import datetime
import uuid
import aiomysql
import json

class BTS_DataStore:
    def __init__(self,
                 db_host = 'localhost',
                 db_port = 3306,
                 database = 'btsc_db',
                 user = 'root',
                 password = 'admin123'):

        self._db_host = db_host
        self._db_port = db_port
        self._db_name = database
        self._db_user = user
        self._db_pwd = password
        self._initialized = False

    async def _initialize(self):
        self._pool = await aiomysql.create_pool(host = 'localhost',
                                                port = self._db_port,
                                                user = self._db_user,
                                                password = self._db_pwd,
                                                db = self._db_name)
        self._initialized = True

    async def store_ride_estimate(self, ride):
        if not self._initialized:
            await self._initialize()

        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute('''INSERT 
                                INTO driver_ride_estimates 
                                    (id, created_at, 
                                    home_city, 
                                    campus, 
                                    available_seats,
                                    total_miles,
                                    co2_emissions,
                                    driver_fare_low,
                                    driver_fare_high,
                                    donation,
                                    wyth_fare,
                                    src_raw_place,
                                    dst_raw_place) 
                                VALUES
                                    (%(id)s,
                                     %(created_at)s,
                                     %(home_city)s,
                                     %(campus)s,
                                     %(available_seats)s,
                                     %(total_miles)s,
                                     %(co2_emissions)s,
                                     %(driver_fare_low)s,
                                     %(driver_fare_high)s,
                                     %(donation)s,
                                     %(wyth_fare)s,
                                     %(src_raw_place)s,
                                     %(dst_raw_place)s)
                            ''',
                           {
                               "id": str(uuid.uuid4()),
                               "created_at": datetime.utcnow(),
                               "home_city": ride['home_city'],
                               "campus": ride['campus'],
                               "available_seats": ride['available_seats'],
                               "total_miles": ride['total_miles'],
                               "co2_emissions": ride['co2_emissions'],
                               "driver_fare_low": ride['driver_fare']['low'],
                               "driver_fare_high": ride['driver_fare']['high'],
                               "donation": ride['donation'],
                               "wyth_fare": ride['wyth_fare'],
                                "src_raw_place": json.dumps({}),
                                "dst_raw_place": json.dumps({})
                           })
                await conn.commit()

    async def store_ride_request_estimate(self, ride):
        if not self._initialized:
            await self._initialize()

        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute('''INSERT 
                                INTO ride_request_estimates 
                                    (id, created_at, 
                                    home_city, 
                                    campus, 
                                    total_miles,
                                    co2_emissions,
                                    rider_offer_low,
                                    rider_offer_high,
                                    donation,
                                    src_raw_place,
                                    dst_raw_place) 
                                VALUES
                                    (%(id)s,
                                     %(created_at)s,
                                     %(home_city)s,
                                     %(campus)s,
                                     %(total_miles)s,
                                     %(co2_emissions)s,
                                     %(rider_offer_low)s,
                                     %(rider_offer_high)s,
                                     %(donation)s,
                                     %(src_raw_place)s,
                                     %(dst_raw_place)s)
                            ''',
                           {
                               "id": str(uuid.uuid4()),
                               "created_at": datetime.utcnow(),
                               "home_city": ride['home_city'],
                               "campus": ride['campus'],
                               "total_miles": ride['total_miles'],
                               "co2_emissions": ride['co2_emissions'],
                               "rider_offer_low": ride['rider_offer']['low'],
                               "rider_offer_high": ride['rider_offer']['high'],
                               "donation": ride['donation'],
                               "src_raw_place": json.dumps({}),
                               "dst_raw_place": json.dumps({})
                           })
                await conn.commit()


    async def store_a_ride(self, ride):
        if not self._initialized:
            await self._initialize()

        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute('''INSERT 
                                INTO driver_rides 
                                    (id, created_at, 
                                    driver_name, 
                                    email,
                                    home_city, 
                                    campus, 
                                    available_seats,
                                    total_miles,
                                    co2_emissions,
                                    driver_fare_low,
                                    driver_fare_high,
                                    donation,
                                    wyth_fare,
                                    src_raw_place,
                                    dst_raw_place) 
                                VALUES
                                    (%(id)s,
                                     %(created_at)s,
                                     %(driver_name)s,
                                     %(email)s,
                                     %(home_city)s,
                                     %(campus)s,
                                     %(available_seats)s,
                                     %(total_miles)s,
                                     %(co2_emissions)s,
                                     %(driver_fare_low)s,
                                     %(driver_fare_high)s,
                                     %(donation)s,
                                     %(wyth_fare)s,
                                     %(src_raw_place)s,
                                     %(dst_raw_place)s)
                            ''',
                           {
                               "id": str(uuid.uuid4()),
                               "created_at": datetime.utcnow(),
                               "driver_name": ride['driver_name'],
                               "email": ride['email'],
                               "home_city": ride['home_city'],
                               "campus": ride['campus'],
                               "available_seats": ride['available_seats'],
                               "total_miles": ride['total_miles'],
                               "co2_emissions": ride['co2_emissions'],
                               "driver_fare_low": ride['driver_fare']['low'],
                               "driver_fare_high": ride['driver_fare']['high'],
                               "donation": ride['donation'],
                               "wyth_fare": ride['wyth_fare'],
                                "src_raw_place": json.dumps(ride['src_raw_place']),
                                "dst_raw_place": json.dumps(ride['dst_raw_place'])
                           })
                await conn.commit()

    async def store_a_rider_ride(self, ride):
        if not self._initialized:
            await self._initialize()

        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute('''INSERT 
                                INTO rider_rides 
                                    (id, created_at, 
                                    rider_name, 
                                    email,
                                    home_city, 
                                    campus, 
                                    total_miles,
                                    co2_emissions,
                                    rider_offer_low,
                                    rider_offer_high,
                                    donation,
                                    src_raw_place,
                                    dst_raw_place) 
                                VALUES
                                    (%(id)s,
                                     %(created_at)s,
                                     %(rider_name)s,
                                     %(email)s,
                                     %(home_city)s,
                                     %(campus)s,
                                     %(total_miles)s,
                                     %(co2_emissions)s,
                                     %(rider_offer_low)s,
                                     %(rider_offer_high)s,
                                     %(donation)s,
                                     %(src_raw_place)s,
                                     %(dst_raw_place)s)
                            ''',
                           {
                               "id": str(uuid.uuid4()),
                               "created_at": datetime.utcnow(),
                               "rider_name": ride['rider_name'],
                               "email": ride['email'],
                               "home_city": ride['home_city'],
                               "campus": ride['campus'],
                               "total_miles": ride['total_miles'],
                               "co2_emissions": ride['co2_emissions'],
                               "rider_offer_low": ride['rider_offer']['low'],
                               "rider_offer_high": ride['rider_offer']['high'],
                               "donation": ride['donation'],
                               "src_raw_place": json.dumps(ride['src_raw_place']),
                               "dst_raw_place": json.dumps(ride['dst_raw_place'])
                           })
                await conn.commit()

    async def store_contact_us(self, contact_us):
        if not self._initialized:
            await self._initialize()

        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute('''INSERT 
                                INTO contact_us 
                                    (id, created_at, 
                                    name, 
                                    email,
                                    subject, 
                                    message) 
                                VALUES
                                    (%(id)s,
                                     %(created_at)s,
                                     %(name)s,
                                     %(email)s,
                                     %(subject)s,
                                     %(message)s)
                            ''',
                           {
                               "id": str(uuid.uuid4()),
                               "created_at": datetime.utcnow(),
                               "name": contact_us.get('name'),
                               "email": contact_us.get('email'),
                               "subject": contact_us.get('subject'),
                               "message": contact_us.get('message')
                           })
                await conn.commit()


    async def get_total_seats_offered(self):
        if not self._initialized:
            await self._initialize()

        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute('''SELECT 
                                        sum(available_seats) as total_seats_offered
                                     FROM 
                                        driver_rides
                                    ''')
                seats_offered = await cur.fetchone()
                seats_offered = int(seats_offered[0]) if seats_offered else 0

                return {"total_seats_offered": seats_offered}

    async def get_total_seats_demanded(self):
        if not self._initialized:
            await self._initialize()

        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute('''SELECT 
                                        count(*) as total_seats_demanded
                                     FROM 
                                        rider_rides
                                    ''')
                seats_offered = await cur.fetchone()
                seats_offered = int(seats_offered[0]) if seats_offered else 0

                return {"total_seats_demanded": seats_offered}

    async def get_participating_colleges(self):
        if not self._initialized:
            await self._initialize()

        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute('''SELECT 
                                        count(distinct(campus)) 
                                     FROM 
                                        rider_rides
                                    ''')
                rider_campus_count = await cur.fetchone()
                rider_campus_count = int(rider_campus_count[0]) if rider_campus_count else 0

                await cur.execute('''SELECT 
                                        count(distinct(campus)) 
                                     FROM 
                                        driver_rides
                                    WHERE 
                                        campus not in (select distinct(campus) from rider_rides)
                                    ''')
                driver_campus_count = await cur.fetchone()
                driver_campus_count = int(driver_campus_count[0]) if driver_campus_count else 0

                return {"n_participating_colleges": rider_campus_count + driver_campus_count}


    async def get_co2_award(self):
        if not self._initialized:
            await self._initialize()

        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                                '''SELECT 
                                    campus, sum(s) as total_co2 
                                FROM 
                                    (   select 
                                            campus, sum(co2_emissions) as s 
                                        from 
                                            driver_rides 
                                        GROUP BY 
                                            campus 
                                    UNION 
                                        select 
                                            campus,sum(co2_emissions) as s 
                                        from 
                                            rider_rides 
                                        GROUP BY
                                            campus
                                    ) as a 
                                GROUP BY 
                                    campus 
                                ORDER BY 
                                    total_co2
                                DESC
                                ''')
                schools_by_co2 = await cur.fetchall()

                response = [{"school": school.split(',')[0],
                             "co2_emissions": int(co2_emissions)}
                            for (school, co2_emissions) in schools_by_co2]

                return response

    async def get_donation_award(self):
        if not self._initialized:
            await self._initialize()

        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                                '''SELECT 
                                    campus, sum(d) as total_donation 
                                FROM 
                                    (   select 
                                            campus, sum(donation) as d 
                                        from 
                                            driver_rides 
                                        GROUP BY 
                                            campus 
                                    UNION 
                                        select 
                                            campus,sum(donation) as d 
                                        from 
                                            rider_rides 
                                        GROUP BY
                                            campus
                                    ) as a 
                                GROUP BY 
                                    campus 
                                ORDER BY 
                                    total_donation
                                DESC
                                ''')
                schools_by_donation = await cur.fetchall()

                response = [{"school": school.format(school).split(',')[0],
                             "donation": int(donation)}
                            for (school, donation) in schools_by_donation]

                return response


    async def get_totals(self):
        if not self._initialized:
            await self._initialize()

        async with self._pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute('''SELECT 
                                        sum(co2_emissions) as total_co2_emissions,
                                        sum(donation) as total_donations
                                     FROM 
                                        driver_rides
                                    ''')
                (total_co2, total_donations) = await cur.fetchone()

                if not total_co2 or int(total_co2) == 0:
                    total_co2 = 1000
                else:
                    total_co2 = int(total_co2)

                if not total_donations or int(total_donations) == 0:
                    total_donations = 100
                else:
                    total_donations = int(total_donations)

                return {"total_co2_emissions": total_co2, #TODO: why it is being returned as Decimal, whereas total_donations as float!
                        "total_donations": total_donations}

