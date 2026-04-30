from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

try:
    import trafilatura
except Exception:  # pragma: no cover
    trafilatura = None


_ADMONITION_CLASSES = {
    "note": "Note",
    "warning": "Warning",
    "tip": "Tip",
    "important": "Important",
    "caution": "Caution",
    "danger": "Danger",
}


class _DocMarkdown(MarkdownConverter):
    def convert_pre(self, el, text, convert_as_inline):  # type: ignore[override]
        code = el.get_text("\n", strip=False)
        lang = ""
        cls = " ".join(el.get("class", []) or [])
        m = re.search(r"language-([a-zA-Z0-9_+-]+)", cls)
        if m:
            lang = m.group(1)
        return f"\n```{lang}\n{code.rstrip()}\n```\n"


def _strip_chrome(soup: BeautifulSoup) -> None:
    for sel in ["nav", "header", "footer", "aside"]:
        for tag in soup.select(sel):
            tag.decompose()

    for cls in ["sidebar", "nav", "navbar", "footer", "header", "toc", "table-of-contents"]:
        for tag in soup.select(f".{cls}"):
            tag.decompose()


def _pick_main(soup: BeautifulSoup) -> Optional[BeautifulSoup]:
    for sel in ["article", "main", "[role=main]", ".content", ".doc-content", ".markdown-body"]:
        tag = soup.select_one(sel)
        if tag and tag.get_text(strip=True):
            return BeautifulSoup(str(tag), "lxml")
    body = soup.body
    if body:
        return BeautifulSoup(str(body), "lxml")
    return soup


def _admonitions_to_blockquotes(md: str) -> str:
    # Very light heuristic: convert lines like "Note:" at start of paragraph to blockquote prefix.
    for key, title in _ADMONITION_CLASSES.items():
        md = re.sub(
            rf"(^|\n)({title}|{key.capitalize()}):\s*(.+)",
            lambda m: f"{m.group(1)}> **{title}**: {m.group(3)}",
            md,
            flags=re.IGNORECASE,
        )
    return md


def html_to_markdown(html: str) -> str:
    extracted_html = None
    if trafilatura is not None:
        try:
            # IMPORTANT: default extract() returns plain text, which loses structure.
            # We request HTML so markdown conversion can preserve headings/lists/code blocks.
            extracted_html = trafilatura.extract(
                html,
                include_comments=False,
                include_tables=True,
                output_format="html",
            )
        except Exception:
            extracted_html = None

    if extracted_html and "<" in extracted_html:
        html = extracted_html

    soup = BeautifulSoup(html, "lxml")
    _strip_chrome(soup)
    main = _pick_main(soup)

    conv = _DocMarkdown(heading_style="ATX", bullets="-")
    md = conv.convert_soup(main) if main else conv.convert_soup(soup)

    md = _admonitions_to_blockquotes(md)
    md = re.sub(r"\n{4,}", "\n\n\n", md).strip() + "\n"
    return md


@dataclass(frozen=True)
class PageDoc:
    title: str
    markdown: str


def extract_title(html: str, fallback: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    t = soup.select_one("title")
    if t and t.get_text(strip=True):
        return t.get_text(strip=True)
    h1 = soup.select_one("h1")
    if h1 and h1.get_text(strip=True):
        return h1.get_text(strip=True)
    return fallback

