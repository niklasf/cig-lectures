# (c) 2020 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>

import aiohttp.web

import cig.db
import cig.view


routes = aiohttp.web.RouteTableDef()


@routes.get("/")
def login(req: aiohttp.web.Request) -> aiohttp.web.Response:
    return aiohttp.web.Response(
        text=cig.view.login().render(),
        content_type="text/html")


def main() -> None:
    app = aiohttp.web.Application()
    app["db"] = cig.db.Database()
    app.add_routes(routes)
    aiohttp.web.run_app(app)
