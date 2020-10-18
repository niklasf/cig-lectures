# (c) 2020 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>

import os.path
import configparser
import logging
import hmac

import aiohttp.web

import cig.db
import cig.view

from typing import List


def normalize_email(email: str) -> str:
    email = email.strip().lower()
    if not all(c.isalnum() or c in "@-." for c in email) or email.count("@") != 1:
        raise ValueError("Invalid email address.")
    if not email.endswith("@tu-clausthal.de"):
        raise ValueError("Please use your address (@tu-clausthal.de).")
    if any(c.isdigit() for c in email):
        raise ValueError("Please use the long form of your email address (with your name).")
    return email


def hmac_email(secret: str, email: str) -> str:
    return hmac.new(secret.encode("utf-8"), f"mailto:{email}".encode("utf-8"), "sha256").hexdigest()


routes = aiohttp.web.RouteTableDef()


@routes.get("/")
def index(_req: aiohttp.web.Request) -> aiohttp.web.Response:
    return aiohttp.web.Response(text=cig.view.index().render(), content_type="text/html")


@routes.get("/{lecture}")
def login(req: aiohttp.web.Request) -> aiohttp.web.Response:
    return aiohttp.web.Response(text=cig.view.login().render(), content_type="text/html")


@routes.post("/{lecture}")
async def login(req: aiohttp.web.Request) -> aiohttp.web.Response:
    form = await req.post()

    try:
        email = normalize_email(form["email"])
    except KeyError:
        raise aiohttp.web.HTTPBadRequest(reason="email required")
    except ValueError as err:
        return aiohttp.web.Response(text=cig.view.login(error=str(err)).render(), content_type="text/html")

    token = hmac_email(req.app["secret"], email)
    print("token:", token)

    return aiohttp.web.Response(text=cig.view.link_sent().render(), content_type="text/html")


def main(argv: List[str]) -> None:
    logging.basicConfig(level=logging.DEBUG)

    config = configparser.ConfigParser()
    config.read([
        os.path.join(os.path.dirname(__file__), "..", "config.default.ini"),
        os.path.join(os.path.dirname(__file__), "..", "config.ini"),
    ] + argv)

    bind = config.get("server", "bind")
    port = config.get("server", "port")

    app = aiohttp.web.Application()
    app["db"] = cig.db.Database()
    app["secret"] = config.get("server", "secret")
    app.add_routes(routes)
    app.router.add_static("/static", os.path.join(os.path.dirname(__file__), "..", "static"))
    try:
        aiohttp.web.run_app(app, host=bind, port=port)
    finally:
        app["db"].close()
