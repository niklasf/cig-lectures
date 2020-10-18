from typing import List, Optional

import cig.data

from cig.data import Lecture
from cig.templating import h, html, raw, url


def layout(title: Optional[str], body: List[h]) -> h:
    return html(lang="de")(
        raw("<!-- https://github.com/niklasf/cig-lectures -->"),
        h("head")(
            h("meta", charset="utf-8"),
            h("meta", name="viewport", content="width=device-width,initial-scale=1"),
            h("title")("CIG Lectures WS2020", f": {title}" if title else None),
            h("link", rel="shortcut icon", href="/static/tuc/favicon.ico"),
        ),
        h("body")(
            h("img", src="/static/tuc/logo.svg"),
            body
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
        h("form", method="POST")(
            error and h("p")(error),
            h("input", type="email", placeholder="max.mustermann@tu-clausthal.de", name="email", required=True),
            h("button", type="submit")("Send login link")
        ),
    ])


def link_sent(*, lecture: Lecture) -> h:
    return layout(lecture.title, [
        h("h1")("Link sent (step 2/3)"),
        h("p")("Check your inbox.")
    ])


def register(*, lecture: Lecture, email: str) -> h:
    return layout(lecture.title, [
        h("h1")("Register for the next ", h("em")(lecture.title), " lecture (step 3/3)"),
        h("h2")("Your contact information"),
        h("p")("You are logged in as ", h("strong")(email), "."),
        h("p")("We do not need additional contact information at this time. But please keep your details updated with the Studentensekretariat."),
        h("h2")("Signup not yet open"),
        h("p")("Singup opens on the day of each lecture.")
    ])
