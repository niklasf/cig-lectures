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
        h("h1")("Step 1: Login"),
        h("form")(
            h("input", type="email", placeholder="max.mustermann@tu-clausthal.de"),
            h("button")("Send login link")
        ),
        h("h1")("Step 2: Sign up for lecture")
    ])
