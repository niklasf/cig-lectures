from typing import List

from cig.templating import h, html, raw


def layout(title: str, body: List[h]) -> h:
    return html(lang="de")(
        raw("<!-- https://github.com/niklasf/cig-lectures -->"),
        h("head")(
            h("meta", charset="utf-8"),
            h("meta", name="viewport", content="width=device-width,initial-scale=1"),
            h("title")("CIG Lectures: ", title)
        ),
        h("body")(body)
    )


def login() -> h:
    return layout("Login", [
        h("h1")("Step 1/3: Login"),
        h("form", method="POST")(
            h("input", type="email", placeholder="max.mustermann@tu-clausthal.de", required=True),
            h("button", type="submit")("Send login link")
        ),
    ])


def link_sent() -> h:
    return layout("Link sent", [
        h("h1")("Step 2/3: Link sent"),
        h("p")("Check your inbox.")
    ])
