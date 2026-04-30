from __future__ import annotations

import hashlib
import re
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from tqdm import tqdm

from .http import HttpClient, canonicalize_url, is_probably_html
from .html_to_md import extract_title, html_to_markdown
from .logging import get_logger
from .models import RunConfig, RunSummary, SourceSpec, SourceType
from .output import IndexItem, make_project_dir, prepend_frontmatter, write_index
from .utils import ensure_dir, guess_name_from_url, safe_filename


_SKIP_PATH_RE = re.compile(
    r"/(blog|pricing|about|cookie|cookies|privacy|terms|legal|login|signin|sign-in|auth|account|changelog)(/|$)",
    re.IGNORECASE,
)

_ASSET_EXTS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".css",
    ".js",
    ".map",
    ".zip",
    ".tar",
    ".gz",
    ".tgz",
    ".exe",
    ".dmg",
    ".mp4",
    ".mp3",
    ".woff",
    ".woff2",
    ".ttf",
    ".ico",
)


@dataclass(frozen=True)
class CrawlItem:
    url: str
    depth: int


def _same_origin(a: str, b: str) -> bool:
    pa, pb = urlparse(a), urlparse(b)
    return pa.scheme == pb.scheme and pa.netloc == pb.netloc


def _looks_like_asset(url: str) -> bool:
    path = urlparse(url).path.lower()
    return path.endswith(_ASSET_EXTS)


def _hash_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _url_to_relpath(url: str) -> Path:
    p = urlparse(url)
    parts = [x for x in p.path.split("/") if x]
    if not parts:
        parts = ["index"]
    if parts[-1].lower().endswith((".html", ".htm")):
        parts[-1] = re.sub(r"\.html?$", "", parts[-1], flags=re.IGNORECASE)
    if p.query:
        parts[-1] = safe_filename(parts[-1] + "-" + p.query.replace("=", "-").replace("&", "-"))
    safe_parts = [safe_filename(x) for x in parts]
    return Path(*safe_parts).with_suffix(".md")


def _extract_links(base_url: str, html: str) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    links: list[str] = []
    for a in soup.select("a[href]"):
        href = (a.get("href") or "").strip()
        if not href:
            continue
        if href.startswith(("mailto:", "tel:", "javascript:")):
            continue
        abs_url = urljoin(base_url, href)
        links.append(abs_url)
    return links


def _try_sitemap(start_url: str, http: HttpClient) -> list[str]:
    p = urlparse(start_url)
    origin = f"{p.scheme}://{p.netloc}"
    sitemap_url = urljoin(origin, "/sitemap.xml")
    try:
        if not http.allowed_by_robots(sitemap_url):
            return []
        r = http.get(sitemap_url)
        if r.status_code >= 400:
            return []
        soup = BeautifulSoup(r.text, "xml")
        urls = [loc.get_text(strip=True) for loc in soup.select("url > loc")]
        return [u for u in urls if u]
    except Exception:
        return []


def crawl_site_to_markdown(spec: SourceSpec, cfg: RunConfig) -> RunSummary:
    log = get_logger()
    if not spec.normalized_url:
        raise ValueError("Missing normalized_url for HTML crawl.")
    start_url = canonicalize_url(spec.normalized_url)
    project_name = guess_name_from_url(start_url)
    out_dir = make_project_dir(cfg.output or Path.cwd(), project_name)

    http = HttpClient.create(cfg.crawl)
    try:
        queue = deque([CrawlItem(url=start_url, depth=0)])
        seen: set[str] = set()
        content_hashes: set[str] = set()
        url_to_md: dict[str, Path] = {}

        # Optional sitemap boost
        for u in _try_sitemap(start_url, http)[: min(2000, cfg.crawl.max_pages * 5)]:
            cu = canonicalize_url(u)
            if cfg.crawl.same_origin_only and not _same_origin(start_url, cu):
                continue
            if cu not in seen:
                queue.append(CrawlItem(url=cu, depth=1))

        summary = RunSummary(source_type=SourceType.html_site, output_dir=out_dir)
        items: list[IndexItem] = []

        progress = tqdm(total=cfg.crawl.max_pages, desc="Crawling", unit="page")
        try:
            while queue and summary.processed_count < cfg.crawl.max_pages:
                item = queue.popleft()
                url = canonicalize_url(item.url)
                if url in seen:
                    continue
                seen.add(url)

                if cfg.crawl.same_origin_only and not _same_origin(start_url, url):
                    summary.skipped_count += 1
                    summary.skipped.append(url)
                    continue
                if _looks_like_asset(url):
                    continue

                if _SKIP_PATH_RE.search(urlparse(url).path) and not urlparse(url).path.startswith(
                    urlparse(start_url).path
                ):
                    continue

                if cfg.crawl.respect_robots and not http.allowed_by_robots(url):
                    continue

                try:
                    r = http.get(url)
                    if r.status_code >= 400:
                        summary.skipped_count += 1
                        summary.skipped.append(url)
                        continue
                    ct = r.headers.get("content-type")
                    if not is_probably_html(ct, url):
                        continue

                    b = r.content
                    h = _hash_bytes(b)
                    if h in content_hashes:
                        continue
                    content_hashes.add(h)

                    html = r.text
                    title = extract_title(html, fallback=url)
                    md = html_to_markdown(html)
                    md = prepend_frontmatter(
                        md,
                        {
                            "page_name": title,
                            "source_url": url,
                            "pull_type": "html",
                        },
                    )

                    rel = _url_to_relpath(url)
                    target = out_dir / rel
                    ensure_dir(target.parent)
                    target.write_text(md, encoding="utf-8")
                    url_to_md[url] = target

                    items.append(IndexItem(title=title, md_path=target))
                    summary.processed_count += 1
                    progress.update(1)

                    if item.depth < cfg.crawl.max_depth:
                        for link in _extract_links(url, html):
                            cu = canonicalize_url(link)
                            if cfg.crawl.same_origin_only and not _same_origin(start_url, cu):
                                continue
                            if cu not in seen:
                                queue.append(CrawlItem(url=cu, depth=item.depth + 1))
                except Exception as e:
                    summary.skipped_count += 1
                    summary.skipped.append(url)
                    summary.warnings.append(f"Failed {url}: {e}")
        finally:
            progress.close()

        # Basic link rewriting pass (markdown links pointing to crawled URLs)
        for url, md_path in url_to_md.items():
            try:
                text = md_path.read_text(encoding="utf-8")
            except Exception:
                continue
            changed = False
            for other_url, other_md in url_to_md.items():
                if other_url == url:
                    continue
                if other_url in text:
                    rel = other_md.relative_to(out_dir).as_posix()
                    text = text.replace(other_url, rel)
                    changed = True
            if changed:
                md_path.write_text(text, encoding="utf-8")

        write_index(out_dir, safe_filename(project_name), items)
        log.ok(f"Crawled {summary.processed_count} pages.")
        return summary
    finally:
        http.close()

