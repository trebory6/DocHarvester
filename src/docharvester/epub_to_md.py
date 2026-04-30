from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup
from ebooklib import epub
from markdownify import MarkdownConverter

from .logging import get_logger
from .models import RunConfig, RunSummary, SourceSpec, SourceType
from .output import IndexItem, make_project_dir, prepend_frontmatter, write_index
from .utils import ensure_dir, safe_filename


class _EpubMarkdown(MarkdownConverter):
    def convert_pre(self, el, text, convert_as_inline):  # type: ignore[override]
        code = el.get_text("\n", strip=False)
        return f"\n```\n{code.rstrip()}\n```\n"


@dataclass(frozen=True)
class Chapter:
    title: str
    html: str


def _download_epub(url: str, dest: Path) -> Path:
    r = httpx.get(url, timeout=120.0, follow_redirects=True)
    r.raise_for_status()
    dest.write_bytes(r.content)
    return dest


def _chapter_title(soup: BeautifulSoup, fallback: str) -> str:
    for sel in ["h1", "title"]:
        t = soup.select_one(sel)
        if t and t.get_text(strip=True):
            return t.get_text(strip=True)
    return fallback


def _html_to_md(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.select("nav, header, footer"):
        tag.decompose()
    conv = _EpubMarkdown(heading_style="ATX", bullets="-")
    md = conv.convert_soup(soup)
    md = "\n".join(ln.rstrip() for ln in md.splitlines()).strip() + "\n"
    return md


def _iter_spine_chapters(book: epub.EpubBook) -> Iterable[Chapter]:
    spine_ids = [sid for sid, _ in book.spine if sid != "nav"]
    for idx, item_id in enumerate(spine_ids, start=1):
        item = book.get_item_with_id(item_id)
        if item is None:
            continue
        if item.get_type() != epub.ITEM_DOCUMENT:
            continue
        try:
            html = item.get_content().decode("utf-8", errors="ignore")
        except Exception:
            continue
        soup = BeautifulSoup(html, "lxml")
        title = _chapter_title(soup, fallback=f"Chapter {idx}")
        text = soup.get_text(" ", strip=True)
        # Skip very small/nav-like docs
        if len(text) < 80:
            continue
        yield Chapter(title=title, html=html)


def convert_epub(spec: SourceSpec, cfg: RunConfig) -> RunSummary:
    log = get_logger()
    out_parent = cfg.output or Path.cwd()

    if spec.source_type == SourceType.epub_local:
        epub_path = Path(spec.local_path or "")
        name = safe_filename(epub_path.stem)
    elif spec.source_type == SourceType.epub_url:
        url = spec.normalized_url or spec.source
        name = safe_filename(Path(urlparse(url).path).stem or "book")
        epub_path = Path("")
    else:
        raise ValueError(f"Unsupported EPUB spec: {spec.source_type}")

    out_dir = make_project_dir(out_parent, f"{name} EPUB")
    summary = RunSummary(source_type=spec.source_type, output_dir=out_dir)

    if spec.source_type == SourceType.epub_url:
        url = spec.normalized_url or spec.source
        epub_path = out_dir / f"{name}.epub"
        _download_epub(url, epub_path)

    try:
        book = epub.read_epub(str(epub_path))
        items: list[IndexItem] = []
        chapter_num = 0
        source_url = epub_path.name

        chapters = list(_iter_spine_chapters(book))
        for i, ch in enumerate(chapters, start=1):
            chapter_num += 1
            md = _html_to_md(ch.html)
            md = prepend_frontmatter(
                md,
                {
                    "page_name": ch.title,
                    "source_url": source_url,
                    "pull_type": "epub",
                },
            )
            filename = f"{i:03d}-{safe_filename(ch.title)}.md"
            md_path = out_dir / filename
            ensure_dir(out_dir)
            md_path.write_text(md, encoding="utf-8")
            items.append(IndexItem(title=ch.title, md_path=md_path))

        summary.processed_count = len(items)
        if not items:
            summary.warnings.append("No readable chapters found in EPUB spine.")

        write_index(out_dir, f"{name} EPUB", items)
        log.ok(f"Converted {summary.processed_count} chapters.")
        return summary
    except Exception as e:
        summary.warnings.append(f"EPUB conversion failed: {e}")
        return summary

