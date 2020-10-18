# (c) 2020 Niklas Fiekas <niklas.fiekas@tu-clausthal.de>

from __future__ import annotations

from urllib.parse import quote as urlquote
from html import escape
from typing import Union, Optional, List, Dict


Attribute = Union[str, bool, None, bool, int, Dict[str, bool]]


def _attribute_name(attr: str) -> str:
    if attr == "klass":
        return "class"
    else:
        attr = attr.rstrip("_")
        assert attr.isalnum()
        return attr


class h:
    def __init__(self, _name: str, **attrs: Attribute):
        assert _name.isalnum()
        self.name = _name

        self.attrs = {_attribute_name(attr): value for attr, value in attrs.items()}
        self.children: Optional[List[Union[h, raw]]] = None

    def __call__(self, *args: Child) -> h:
        if self.children is None:
            self.children = []
        for arg in args:
            if arg is None:
                continue
            elif isinstance(arg, list):
                self.__call__(*arg)
            elif isinstance(arg, (h, raw)):
                self.children.append(arg)
            else:
                self.children.append(raw(escape(str(arg), quote=False)))
        return self

    def render_into(self, builder: List[str]) -> None:
        builder.append("<")
        builder.append(self.name)
        for attr, value in self.attrs.items():
            if value is False or value is None:
                continue
            builder.append(" ")
            builder.append(attr)
            if value is True:
                continue
            if isinstance(value, list):
                value = " ".join(value)
            elif isinstance(value, dict):
                value = " ".join(key for key, val in value.items() if val)
            builder.append("=\"")
            builder.append(escape(str(value)))
            builder.append("\"")
        builder.append(">")
        if self.children is not None:
            for child in self.children:
                child.render_into(builder)
            builder.append("</")
            builder.append(self.name)
            builder.append(">")

    def render(self) -> str:
        builder: List[str] = []
        self.render_into(builder)
        return "".join(builder)


class raw:
    def __init__(self, html: str):
        self.html = html

    def render_into(self, builder: List[str]) -> None:
        builder.append(self.html)


class html(h):
    def __init__(self, **attrs: Attribute):
        super().__init__("html", **attrs)

    def render_into(self, builder: List[str]) -> None:
        builder.append("<!DOCTYPE html>")
        super().render_into(builder)


Child = Union[str, h, raw, None, int, List[Union[str, h, raw, None, int]]]


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
