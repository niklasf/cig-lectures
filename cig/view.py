# (c) 2020 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>

import pytz
import datetime
import itertools

import cig.data
import cig.db

from cig.db import Registrations, Row
from cig.data import Lecture
from cig.example_quiz import Statement
from tinyhtml import Frag, h, html, raw, frag
from urllib.parse import quote as urlquote
from typing import List, Optional, Callable, Union


def layout(title: Optional[str], body: Frag) -> Frag:
    return html(lang="de")(
        raw("<!-- https://github.com/niklasf/cig-lectures -->"),
        h("head")(
            h("meta", charset="utf-8"),
            h("meta", name="viewport", content="width=device-width,initial-scale=1"),
            h("title")("CIG Lectures WS2020", f": {title}" if title else None),
            h("link", rel="stylesheet", href="/static/style.css"),
            h("link", rel="shortcut icon", href="/static/tuc/favicon.ico"),
        ),
        h("body")(
            h("header")(
                h("img", src="/static/tuc/logo.svg", klass="no-print"),
            ),
            h("main")(body),
            h("footer")(
                "Server time: ", cig.db.now().strftime("%d.%m.%Y %H:%M:%S"), ". ",
                "This program is free/libre open source software. ",
                h("a", href="https://github.com/niklasf/cig-lectures")("GitHub"), ".",
            ),
        ),
    )


def index() -> Frag:
    return layout(None, frag(
        h("h1")("CIG Lectures WS2020"),
        h("ul")(
            h("li")(
                h("a", href=url(name))(lecture.title)
            ) for name, lecture in cig.data.LECTURES.items()
        ),
    ))


def login(*, title: str, h1: Frag, error: Optional[str] = None) -> Frag:
    return layout(title, frag(
        h("h1")(h1),
        h("section")(
            h("form", method="POST")(
                error and h("p", klass="error")(error),
                h("p")(
                    h("label", for_="email")("Email:"),
                    " ",
                    h("input", type="email", placeholder="max.mustermann@tu-clausthal.de", id="email", name="email", required=True),
                ),
                h("p")(h("button", type="submit")("Send login link")),
            )
        )
    ))


def login_lecture(*, lecture: Lecture, error: Optional[str] = None) -> Frag:
    return login(
        title=lecture.title,
        h1=frag("Register for the next ", h("em")(lecture.title), " lecture (step 1/3)"),
        error=error,
    )


def login_quiz(*, lecture: Lecture, error: Optional[str] = None) -> Frag:
    return login(
        title=lecture.title,
        h1=frag("Login for ", h("em")(lecture.title), " self assessment quiz"),
        error=error,
    )


def link_sent(*, title: str, email_text: Optional[str]) -> Frag:
    return layout(title, frag(
        h("h1")(title),
        h("section")(
            h("p")("Check your inbox."),
            h("p")(
                "Development mode enabled. This email would have been sent: ",
                h("pre")(email_text),
            ) if email_text else None,
        )
    ))


def register(*, lecture: Lecture, email: str, events: List[Registrations], admin: bool = False, today: datetime.date) -> Frag:
    def modifier(row: Row) -> Callable[[str], Frag]:
        if row.deleted and row.admin:
            return lambda *children: h("del")(h("ins")(*children))
        elif row.deleted:
            return h("del")
        elif row.admin:
            return h("ins")
        else:
            return h("span")

    return layout(lecture.title, frag(
        h("h1", klass="no-print")("Register for the next ", h("em")(lecture.title), " lecture (step 3/3)"),
        h("section")(
            h("h2")("Signup not open, yet"),
            h("p")("Signup opens on the day of each lecture. Please come only after you have successfully reserved a seat."),
        ) if not events else [
            h("section", klass={
                "not-today": registrations.event.date != today,
            })(
                h("h2", id=f"event-{registrations.event.id}")(
                    registrations.event.title, " (", registrations.event.date.strftime("%a, %d.%m."), ")",
                ),
                h("p")("Please reserve a seat only if you will physically attend this lecture in ", h("strong")(registrations.event.location), " on this particular day."),
                h("p")("Please come only after you successfully reserved a seat. There are ", h("strong")(f"{registrations.event.seats} seats"), " in total."),
                h("table")(
                    h("thead")(
                        h("tr")(
                            h("th")("Seat"),
                            h("th")("Name"),
                            h("th")("Status"),
                            h("th", klass="no-print")("Admin") if admin else None,
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
                                "Reservation deleted by admin" if row.deleted else row.time.strftime("Successfully registered %d.%m. %H:%M" if row.n is not None and row.n <= registrations.event.seats else "Seat not available (%d.%m. %H:%M). We will make sure to provide the lecture materials online."),
                            ),
                            h("td", klass="no-print")(
                                h("form", method="POST")(
                                    h("input", type="hidden", name="name", value=row.name),
                                    h("input", type="hidden", name="restore" if row.deleted else "delete", value=registrations.event.id),
                                    h("button")("Restore" if row.deleted else "Delete"),
                                )
                            ) if admin else None,
                        ) for row in registrations.rows() if row.name == email or admin
                    ])
                ) if admin or registrations.has(email) else None,
                h("form", method="POST", onsubmit="return confirm('Please register only if you will physically attend the lecture on this particular day.')" if not admin else None)(
                    h("input", type="text", name="name", placeholder=email) if admin else None,
                    h("input", type="hidden", name="reserve", value=registrations.event.id),
                    h("button", type="submit")("Reserve seat (admin)" if admin else "Reserve seat"),
                ) if admin or not registrations.has(email) else None,
            ) for registrations in events
        ],
        h("section", klass="no-print")(
            h("h2")("Your contact information"),
            h("p")("You are logged in as ", h("strong")(email), "."),
            h("p")("We do not need additional contact information at this time. But please keep your details updated with the Studentensekretariat."),
        ),
    ))


def quiz(*, email: Optional[str], statements: List[Statement], answers: Optional[List[bool]], correct: Optional[int]) -> Frag:
    return layout("Complexity Theory", frag(
        h("h1")(h("em")("Complexity Theory"), " self assessment quiz"),
        frag(
            h("h2")("What is saved?"),
            h("ul")(
                h("li")("That you, ", h("strong")(email), ", participated"),
                h("li")("Your answers"),
                h("li")("But no connection between these two"),
            ),
        ) if email is not None else None,
        h("h2")("True or false?"),
        h("p")(
            "These following are considered basic questions from ", h("em")("Informatics III"), ". ",
            "Use these in your decision, if you're ready to take the course. ",
            "Your answers are anonymous (and therefore obviously not graded).",
        ),
        h("form", method="POST")(
            h("table")(
                h("tr", klass={
                    "correct": answer is statement.truth,
                    "incorrect": answer is (not statement.truth),
                })(
                    h("td")(i, "."),
                    h("td")(statement.text),
                    h("td")(
                        h("input", type="radio", name=f"stmt-{i}", id=f"stmt-{i}-1", value=1, required=True, checked=answer is True, disabled=answer is not None),
                        h("label", for_=f"stmt-{i}-1")("True"),
                    ),
                    h("td")(
                        h("input", type="radio", name=f"stmt-{i}", id=f"stmt-{i}-0", value=0, required=True, checked=answer is False, disabled=answer is not None),
                        h("label", for_=f"stmt-{i}-0")("False"),
                    ),
                ) for i, statement, answer in itertools.zip_longest(range(len(statements)), statements, answers or [])
            ),
            h("button", type="submit")("Submit answers") if not answers else None,
            h("p")("You scored ", h("strong")(round(correct / len(statements) * 100), "%"), ".") if correct is not None else None,
        ),
    ))


def url(*segments: Union[str, int], **query: Union[str, int]) -> str:
    builder = []
    if not segments:
        builder.append("/")
    else:
        for segment in segments:
            builder.append("/")
            builder.append(urlquote(str(segment), safe=""))
    first = True
    for arg, value in query.items():
        builder.append("?" if first else "&")
        first = False
        builder.append(urlquote(arg, safe=""))
        builder.append("=")
        builder.append(urlquote(str(value)))
    return "".join(builder)
