# (c) 2020 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>

import os.path
import configparser
import datetime
import logging
import hmac

import aiohttp
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
async def index(_req: aiohttp.web.Request) -> aiohttp.web.Response:
    # Show list of lectures.
    return aiohttp.web.Response(text=cig.view.index().render(), content_type="text/html")


def extract_lecture(req: aiohttp.web.Request) -> Lecture:
    try:
        return cig.data.LECTURES[req.match_info["lecture"]]
    except KeyError:
        raise aiohttp.web.HTTPNotFound(reason="lecture not found")


def extract_verified_email(req: aiohttp.web.Request) -> Optional[str]:
    email: str = req.query.get("email", "")
    token = req.query.get("hmac", "")
    if hmac.compare_digest(hmac_email(req.app["secret"], email), token):
        return email
    else:
        return None


@routes.get("/{lecture}")
async def get_lecture(req: aiohttp.web.Request) -> aiohttp.web.Response:
    lecture = extract_lecture(req)
    email = extract_verified_email(req)
    admin = email is not None and req.query.get("admin", "") == "yes" and cig.data.admin(email)
    if not email:
        # Show login form.
        return aiohttp.web.Response(text=cig.view.login(lecture=lecture).render(), content_type="text/html")
    else:
        # Show registration form.
        today = datetime.date.today()
        events = [
            req.app["db"].registrations(event=event) for event in cig.data.EVENTS.values()
            if event.lecture == lecture.id and (event.date == today or (admin and abs(event.date - today) <= datetime.timedelta(days=14)))
        ]
        return aiohttp.web.Response(
            text=cig.view.register(lecture=lecture, email=email, events=events, admin=admin, today=today).render(),
            content_type="text/html")


@routes.post("/{lecture}")
async def post_lecture(req: aiohttp.web.Request) -> aiohttp.web.StreamResponse:
    lecture = extract_lecture(req)
    email = extract_verified_email(req)
    admin = email is not None and cig.data.admin(email)
    form = await req.post()

    if not email:
        # Process login form.
        try:
            email = normalize_email(str(form["email"]))
        except KeyError:
            raise aiohttp.web.HTTPBadRequest(reason="email required")
        except ValueError as err:
            return aiohttp.web.Response(text=cig.view.login(lecture=lecture, error=str(err)).render(), content_type="text/html")

        token = hmac_email(req.app["secret"], email)
        magic_link = req.app["base_url"].rstrip("/") + cig.templating.url(req.match_info["lecture"], email=email, hmac=token)
        print(magic_link)


        email_text = []
        email_text.append(f"Continue here: {magic_link}")
        if cig.data.admin(email):
            email_text.append("")
            email_text.append(f"Admin interface: {magic_link}&admin=yes")
        email_text.append("")
        email_text.append("You can also bookmark this link for future lectures.")
        email_text.append("")
        email_text.append("---")
        email_text.append(f"Automated email on behalf of {lecture.lecturer} and team")

        if not req.app["dev"]:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://api.mailgun.net/v3/{req.app['mailgun_domain']}/messages",
                    auth=aiohttp.BasicAuth("api", req.app["mailgun_key"]),
                    data={
                        "from": f"CIG Lectures <noreply@{req.app['mailgun_domain']}>",
                        "to": email,
                        "subject": f"Register for the next {lecture.title} lecture (step 2/3)",
                        "text": "\n".join(email_text),
                    }
                ) as res:
                    print("Response:", res.status, "-", await res.text())

        return aiohttp.web.Response(
            text=cig.view.link_sent(lecture=lecture, email_text="\n".join(email_text) if req.app["dev"] else None).render(),
            content_type="text/html")
    else:
        # Process registration form.
        try:
            event = cig.data.EVENTS[int(str(form["reserve"]))]
        except (KeyError, ValueError):
            pass
        else:
            name = str(form.get("name", email)).strip() if admin else email
            if "@" in name:
                name = name.lower()
            if name and (admin or event.date == datetime.date.today()):
                req.app["db"].maybe_register(event=event.id, name=name, admin=admin)

        # Process admin actions on registration form.
        if admin:
            try:
                delete = int(str(form["delete"]))
                name = str(form["name"])
            except (KeyError, ValueError):
                pass
            else:
                req.app["db"].delete(event=delete, name=name)

            try:
                restore = int(str(form["restore"]))
                name = str(form["name"])
            except (KeyError, ValueError):
                pass
            else:
                req.app["db"].restore(event=restore, name=name)

        return await get_lecture(req)


def main(argv: List[str]) -> None:
    logging.basicConfig(level=logging.DEBUG)

    config = configparser.ConfigParser()
    config.read([
        os.path.join(os.path.dirname(__file__), "..", "config.default.ini"),
        os.path.join(os.path.dirname(__file__), "..", "config.ini"),
    ] + argv)

    bind = config.get("server", "bind")
    port = config.getint("server", "port")

    app = aiohttp.web.Application()
    app["base_url"] = config.get("server", "base_url")
    app["db"] = cig.db.Database()
    app["dev"] = config.getboolean("server", "dev")
    app["secret"] = config.get("server", "secret")
    app["mailgun_domain"] = config.get("mailgun", "domain")
    app["mailgun_key"] = config.get("mailgun", "key")
    app.add_routes(routes)
    app.router.add_static("/static", os.path.join(os.path.dirname(__file__), "..", "static"))

    try:
        aiohttp.web.run_app(app, host=bind, port=port, access_log=None)
    finally:
        app["db"].close()
