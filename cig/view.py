# (c) 2020 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>

import datetime

import cig.data

from cig.db import Registrations, Row
from cig.data import Lecture
from cig.templating import h, html, raw, url
from typing import List, Optional, Callable


def layout(title: Optional[str], body: h) -> h:
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
            h("header")(
                h("img", src="/static/tuc/logo.svg", klass="no-print"),
            ),
            body,
            h("footer", klass="no-print")(
                "This program is free/libre open source software. ",
                h("a", href="https://github.com/niklasf/cig-lectures")("GitHub"), "."
            )
        )
    )


def index() -> h:
    return layout(None, h("main")(
        h("h1")("CIG Lectures WS2020"),
        h("ul")([
            h("li")(
                h("a", href=url(name))(lecture.title)
            ) for name, lecture in cig.data.LECTURES.items()
        ])
    ))


def login(*, lecture: Lecture, error: Optional[str] = None) -> h:
    return layout(lecture.title, h("main")(
        h("h1")("Register for the next ", h("em")(lecture.title), " lecture (step 1/3)"),
        h("section")(
            h("form", method="POST")(
                error and h("p", klass="error")(error),
                h("p")(
                    h("label", for_="email")("Email:"),
                    " ",
                    h("input", type="email", placeholder="max.mustermann@tu-clausthal.de", id="email", name="email", required=True)
                ),
                h("p")(h("button", type="submit")("Send login link"))
            )
        )
    ))


def link_sent(*, lecture: Lecture, email_text: Optional[str]) -> h:
    return layout(lecture.title, h("main")(
        h("h1")("Link sent (step 2/3)"),
        h("section")(
            h("p")("Check your inbox."),
            h("p")(
                "Development mode enabled. This email would have been sent: ",
                h("pre")(email_text)
            ) if email_text else None
        )
    ))


def register(*, lecture: Lecture, email: str, events: List[Registrations], admin: bool = False, today: datetime.date) -> h:
    def modifier(row: Row) -> Callable[[str], h]:
        if row.deleted and row.admin:
            return lambda *children: h("del")(h("ins")(*children))
        elif row.deleted:
            return h("del")
        elif row.admin:
            return h("ins")
        else:
            return h("span")

    return layout(lecture.title, h("main")(
        h("h1", klass="no-print")("Register for the next ", h("em")(lecture.title), " lecture (step 3/3)"),
        h("section", klass="no-print")(
            h("h2")("Your contact information"),
            h("p")("You are logged in as ", h("strong")(email), "."),
            h("p")("We do not need additional contact information at this time. But please keep your details updated with the Studentensekretariat.")
        ),
        h("section")(
            h("h2")("Signup not open, yet"),
            h("p")("Signup opens on the day of each lecture.")
        ) if not events else [
            h("section", klass={
                "not-today": registrations.event.date != today,
            })(
                h("h2", id=f"event-{registrations.event.id}")(
                    registrations.event.title, " (", registrations.event.date.strftime("%a, %d.%m."), ")"
                ),
                h("p")("Please reserve a seat only if you will physically attend this lecture in ", h("strong")(registrations.event.location), "."),
                h("p")("Please come only after you successfully reserved a seat. There are ", h("strong")(f"{registrations.event.seats} seats"), " in total."),
                h("table")(
                    h("thead")(
                        h("tr")(
                            h("th")("Seat"),
                            h("th")("Name"),
                            h("th")("Status"),
                            h("th", klass="no-print")("Admin") if admin else None
                        )
                    ),
                    h("tbody")([
                        h("tr", klass={
                            "me": row.name == email,
                            "overhang": row.n is not None and row.n > registrations.event.seats,
                        })(
                            h("td")(modifier(row)(f"#{row.n}") if row.n is not None else ""),
                            h("td")(modifier(row)(row.name)),
                            h("td")(
                                "Reservation deleted by admin" if row.deleted else row.time.strftime("Successfully registered %d.%m. %H:%m" if row.n is not None and row.n <= registrations.event.seats else "Seat not available (%d.%m. %H:%m). We will make sure to provide the lecture materials online.")
                            ),
                            h("td", klass="no-print")(
                                h("form", method="POST")(
                                    h("input", type="hidden", name="name", value=row.name),
                                    h("input", type="hidden", name="restore" if row.deleted else "delete", value=registrations.event.id),
                                    h("button")("Restore" if row.deleted else "Delete")
                                )
                            ) if admin else None
                        ) for row in registrations.rows() if row.name == email or admin
                    ])
                ) if admin or registrations.has(email) else None,
                h("form", method="POST", onsubmit="return confirm('Please register only if you will physically attend this lecture.')" if not admin else None)(
                    h("input", type="text", name="name", placeholder=email) if admin else None,
                    h("input", type="hidden", name="reserve", value=registrations.event.id),
                    h("button", type="submit")("Reserve seat (admin)" if admin else "Reserve seat")
                ) if admin or not registrations.has(email) else None,
            ) for registrations in events
        ]
    ))
