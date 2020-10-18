# (c) 2020 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>

import os.path
import datetime
import configparser
import datetime
import logging
import hmac

import aiohttp.web

import cig.db
import cig.view
import cig.templating

from typing import List, Optional
from cig.data import Lecture


def normalize_email(email: str) -> str:
    email = email.strip().lower()
    if not all(c.isalnum() or c in "@-." for c in email) or email.count("@") != 1 or email.startswith("@"):
        raise ValueError("Invalid email address.")
    if not email.endswith("@tu-clausthal.de"):
        raise ValueError("Please use your university email address (@tu-clausthal.de).")
    if any(c.isdigit() for c in email):
        raise ValueError("Please use the long form of your email address (with your name).")
    return email


def hmac_email(secret: str, email: str) -> str:
    return hmac.new(secret.encode("utf-8"), f"mailto:{email}".encode("utf-8"), "sha256").hexdigest()


routes = aiohttp.web.RouteTableDef()


@routes.get("/")
def index(_req: aiohttp.web.Request) -> aiohttp.web.Response:
    return aiohttp.web.Response(text=cig.view.index().render(), content_type="text/html")


def extract_lecture(req: aiohttp.web.Request) -> Lecture:
    try:
        return cig.data.LECTURES[req.match_info["lecture"]]
    except KeyError:
        raise aiohttp.web.HTTPNotFound(reason="lecture not found")


def extract_verified_email(req: aiohttp.web.Request) -> Optional[str]:
    email = req.query.get("email", "")
    token = req.query.get("hmac", "")
    if hmac.compare_digest(hmac_email(req.app["secret"], email), token):
        return email
    else:
        return None


@routes.get("/{lecture}")
def get_lecture(req: aiohttp.web.Request) -> aiohttp.web.Response:
    lecture = extract_lecture(req)
    email = extract_verified_email(req)
    admin = cig.data.admin(email)
    if not email:
        return aiohttp.web.Response(text=cig.view.login(lecture=lecture).render(), content_type="text/html")
    else:
        today = datetime.date.today()
        events = [
            req.app["db"].registrations(event=event) for event in cig.data.EVENTS.values()
            if event.lecture == lecture.id and (event.date == today or (admin and abs(event.date - today) <= datetime.timedelta(days=2)))
        ]
        return aiohttp.web.Response(
            text=cig.view.register(lecture=lecture, email=email, events=events, admin=admin, today=today).render(),
            content_type="text/html")


@routes.post("/{lecture}")
async def post_lecture(req: aiohttp.web.Request) -> aiohttp.web.Response:
    lecture = extract_lecture(req)
    email = extract_verified_email(req)
    admin = cig.data.admin(email)
    form = await req.post()

    if not email:
        try:
            email = normalize_email(form["email"])
        except KeyError:
            raise aiohttp.web.HTTPBadRequest(reason="email required")
        except ValueError as err:
            return aiohttp.web.Response(text=cig.view.login(lecture=lecture, error=str(err)).render(), content_type="text/html")

        token = hmac_email(req.app["secret"], email)
        print(req.app["base_url"].rstrip("/") + cig.templating.url(req.match_info["lecture"], email=email, hmac=token))
        return aiohttp.web.Response(text=cig.view.link_sent(lecture=lecture).render(), content_type="text/html")
    else:
        try:
            event = cig.data.EVENTS[int(form["reserve"])]
        except (KeyError, ValueError):
            pass
        else:
            name = form.get("name", email).strip() if admin else email
            if "@" in name:
                name = name.lower()
            if name and (admin or event.date == datetime.date.today()):
                req.app["db"].maybe_register(event=event.id, name=name, admin=admin)

        if admin:
            try:
                event = int(form["delete"])
                name = form["name"]
            except (KeyError, ValueError):
                pass
            else:
                req.app["db"].delete(event=event, name=name)

            try:
                event = int(form["restore"])
                name = form["name"]
            except (KeyError, ValueError):
                pass
            else:
                req.app["db"].restore(event=event, name=name)

        return get_lecture(req)


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
    app["base_url"] = config.get("server", "base_url")
    app["db"] = cig.db.Database()
    app["secret"] = config.get("server", "secret")
    app.add_routes(routes)
    app.router.add_static("/static", os.path.join(os.path.dirname(__file__), "..", "static"))
    try:
        aiohttp.web.run_app(app, host=bind, port=port)
    finally:
        app["db"].close()
