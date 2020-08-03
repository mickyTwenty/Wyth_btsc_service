from functools import partial
from aiohttp import web
from app.handlers import Handlers
import aiohttp_cors

HOST = 'localhost'
PORT= 3306
DB_NAME = 'address_book'
USER = 'root'
PASSWORD = 'Wyth123!!!'

class RestApp:

    def __init__(self, port):
        self._port = port
        self.handlers = Handlers()

        self._app = web.Application()
        self._app.router.add_routes([#web.get('/drivers/estimates', self.handlers.trip_estimates_handler),
                                     #web.get('/riders/estimates', partial(self.handlers.trip_estimates_handler, driver_mode = False)),
                                     #web.post('/drivers/trips', self.handlers.post_new_ride_handler),
                                     #web.post('/riders/trips', self.handlers.post_new_rider_trip_handler),
                                     #web.get('/totals', self.handlers.get_totals),
                                     web.get('/totals/co2', self.handlers.get_total_co2_handler),
                                     web.get('/totals/charity', self.handlers.get_total_charity_handler)])
        
        cors = aiohttp_cors.setup(self._app)
        resource = cors.add(self._app.router.add_resource("/totals"))
        route = cors.add(
        resource.add_route("GET", self.handlers.get_totals), {
            "*": aiohttp_cors.ResourceOptions(
                expose_headers="*",
                allow_headers="*"),
        })

        resource = cors.add(self._app.router.add_resource("/drivers/estimates"))
        route = cors.add(
        resource.add_route("POST", self.handlers.trip_estimates_handler), {
            "*": aiohttp_cors.ResourceOptions(
                expose_headers="*",
                allow_headers="*"),
        })


        resource = cors.add(self._app.router.add_resource("/riders/estimates"))
        route = cors.add(
        resource.add_route("POST", partial(self.handlers.trip_estimates_handler, driver_mode = False)), {
            "*": aiohttp_cors.ResourceOptions(
                expose_headers="*",
                allow_headers="*"),
        })

        resource = cors.add(self._app.router.add_resource("/drivers/trips"))
        cors.add(
        resource.add_route("POST", self.handlers.post_new_ride_handler), {
            "*": aiohttp_cors.ResourceOptions(
                expose_headers="*",
                allow_headers="*"),
        })

        resource = cors.add(self._app.router.add_resource("/riders/trips"))
        cors.add(
        resource.add_route("POST", self.handlers.post_new_rider_trip_handler), {
            "*": aiohttp_cors.ResourceOptions(
                expose_headers="*",
                allow_headers="*"),
        })

        resource = cors.add(self._app.router.add_resource("/contact_us"))
        cors.add(
        resource.add_route("POST", self.handlers.contact_us_handler), {
            "*": aiohttp_cors.ResourceOptions(
                expose_headers="*",
                allow_headers="*"),
        })


    def start(self):
        print('starting BTS-challenge servic {}'.format(self._port))
        web.run_app(app=self._app, port=self._port)

if __name__ == '__main__':
    rest_app = RestApp(8080)
    rest_app.start()