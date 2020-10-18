from typing import List, Optional

import cig.data

from cig.db import Registrations
from cig.data import Lecture, Event
from cig.templating import h, html, raw, url


def layout(title: Optional[str], body: List[h]) -> h:
    return html(lang="de")(
        raw("<!-- https://github.com/niklasf/cig-lectures -->"),
        h("head")(
            h("meta", charset="utf-8"),
            h("meta", name="viewport", content="width=device-width,initial-scale=1"),
            h("title")("CIG Lectures WS2020", f": {title}" if title else None),
            h("link", rel="stylesheet", href="/static/style.css"),
            h("link", rel="shortcut icon", href="/static/tuc/favicon.ico")
        ),
        h("body")(
            h("main")(
                h("img", src="/static/tuc/logo.svg", klass="no-print"),
                body
            )
        )
    )


def index() -> h:
    return layout(None, [
        h("h1")("CIG Lectures WS2020"),
        h("ul")([
            h("li")(
                h("a", href=url(name))(lecture.title)
            ) for name, lecture in cig.data.LECTURES.items()
        ])
    ])


def login(*, lecture: Lecture, error: Optional[str] = None) -> h:
    return layout(lecture.title, [
        h("h1")(f"Register for the next ", h("em")(lecture.title), " lecture (step 1/3)"),
        h("section")(
            h("form", method="POST")(
                error and h("p", klass="error")(error),
                h("p")(
                    h("label", for_="email")("E-Mail:"),
                    " ",
                    h("input", type="email", placeholder="max.mustermann@tu-clausthal.de", id="email", name="email", required=True)
                ),
                h("p")(h("button", type="submit")("Send login link"))
            )
        ),
    ])


def link_sent(*, lecture: Lecture) -> h:
    return layout(lecture.title, [
        h("h1")("Link sent (step 2/3)"),
        h("section")(
            h("p")("Check your inbox.")
        )
    ])


def register(*, lecture: Lecture, email: str, events: List[Registrations], admin: bool = False) -> h:
    return layout(lecture.title, [
        h("h1", klass="no-print")("Register for the next ", h("em")(lecture.title), " lecture (step 3/3)"),
        h("section", klass="no-print")(
            h("h2")("Your contact information"),
            h("p")("You are logged in as ", h("strong")(email), "."),
            h("p")("We do not need additional contact information at this time. But please keep your details updated with the Studentensekretariat.")
        ),
        h("section")(
            h("h2")("Signup not yet open"),
            h("p")("Singup opens on the day of each lecture.")
        ) if not events else [
            h("section")(
                h("h2")(registrations.event.title, " (", registrations.event.date.strftime("%a, %d.%m."), ")"),
                h("p")("Please reserve a seat only if you will physically attend this lecture in ", h("strong")(registrations.event.location), "."),
                h("p")("Please come only after you successfully reserved a seat. There are ", h("strong")(f"{registrations.event.seats} seats"), " in total."),
                h("table")(
                    h("thead")(
                        h("tr")(
                            h("th")("Seat"),
                            h("th")("Name"),
                            h("th")("Status")
                        )
                    ),
                    h("tbody")([
                        h("tr", klass={
                            "me": row.name == email,
                            "overhang": row.n > registrations.event.seats,
                        })(
                            h("td")(row.n),
                            h("td")(row.name),
                            h("td")(
                                row.time.strftime("Successfully registered %d.%m. %H:%m" if row.n <= registrations.event.seats else "No seat is available (%d.%m. %H:%m). We will make sure to provide the lecture materials online.")
                            )
                        ) for row in registrations.rows() if row.name == email or admin
                    ])
                ) if admin or registrations.has(email) else None,
                h("form", method="POST")(
                    h("input", type="text", name="name", placeholder=email) if admin else None,
                    h("input", type="hidden", name="reserve", value=registrations.event.id),
                    h("button", type="submit")("Reserve seat (admin)" if admin else "Reserve seat")
                ) if admin or not registrations.has(email) else None,
            ) for registrations in events
        ]
    ])
