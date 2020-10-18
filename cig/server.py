# (c) 2020 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>

import hmac

import aiohttp.web

import cig.db
import cig.view


def normalize_email(email):
    email = email.strip().lower()
    if not all(c.isalnum() or c in "@-." for c in email) or email.count("@") != 1:
        raise ValueError("Invalid email address")
    if not email.endswith("@tu-clausthal.de"):
        raise ValueError("Please use your address (@tu-clausthal.de)")
    if any(c.isdigit() for c in email):
        raise ValueError("Please use the long form of your email address (with your name)")
    return email


routes = aiohttp.web.RouteTableDef()


@routes.get("/")
def login(req: aiohttp.web.Request) -> aiohttp.web.Response:
    return aiohttp.web.Response(
        text=cig.view.login().render(),
        content_type="text/html")


@routes.post("/")
async def login(req: aiohttp.web.Request) -> aiohttp.web.Response:
    form = await req.post()

    try:
        email = normalize_email(form["email"])
    except KeyError:
        raise aiohttp.web.HTTPBadRequest(reason="email required")
    except ValueError as err:
        return aiohttp.web.Response(text=cig.view.login(error=str(err)).render(), content_type="text/html")

    return aiohttp.web.Response(
        text=cig.view.link_sent().render(),
        content_type="text/html")


def main() -> None:
    app = aiohttp.web.Application()
    app["db"] = cig.db.Database()
    app["secret"] = "TODO"
    app.add_routes(routes)
    try:
        aiohttp.web.run_app(app)
    finally:
        app["db"].close()
