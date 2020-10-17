# (c) 2020 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>

import aiohttp.web

import cig.db


routes = aiohttp.web.RouteTableDef()


def main() -> None:
    app = aiohttp.web.Application()
    app["db"] = cig.db.Database()
    app.add_routes(routes)
    aiohttp.web.run_app(app)
