from typing import List, Optional

import cig.data
from cig.templating import h, html, raw, url


def layout(title: str, body: List[h]) -> h:
    return html(lang="de")(
        raw("<!-- https://github.com/niklasf/cig-lectures -->"),
        h("head")(
            h("meta", charset="utf-8"),
            h("meta", name="viewport", content="width=device-width,initial-scale=1"),
            h("title")("CIG Lectures: ", title),
            h("link", rel="shortcut icon", href="/static/tuc/favicon.ico"),
        ),
        h("body")(
            h("img", src="/static/tuc/logo.svg"),
            body
        )
    )


def index() -> h:
    return layout("CIG Lectures WS2020", [
        h("h1")("CIG Lectures WS2020"),
        h("ul")([
            h("li")(
                h("a", href=url(name))(lecture.title)
            ) for name, lecture in cig.data.LECTURES.items()
        ])
    ])


def login(*, error: Optional[str] = None) -> h:
    return layout("Login", [
        h("h1")("Step 1/3: Login"),
        h("form", method="POST")(
            error and h("p")(error),
            h("input", type="email", placeholder="max.mustermann@tu-clausthal.de", name="email", required=True),
            h("button", type="submit")("Send login link")
        ),
    ])


def link_sent() -> h:
    return layout("Link sent", [
        h("h1")("Step 2/3: Link sent"),
        h("p")("Check your inbox.")
    ])
