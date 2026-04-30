from __future__ import annotations

import re
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from .http import HttpClient, is_probably_epub, is_probably_html, is_probably_pdf
from .logging import get_logger
from .models import RunConfig, RunSummary, SourceSpec, SourceType
from .utils import looks_like_url, normalize_url


_GITHUB_REPO_RE = re.compile(r"^/([^/]+)/([^/]+?)(?:\.git)?/?$")


def _detect_github_repo(url: str) -> Optional[tuple[str, str]]:
    p = urlparse(url)
    if p.netloc.lower() != "github.com":
        return None
    m = _GITHUB_REPO_RE.match(p.path)
    if not m:
        return None
    owner, repo = m.group(1), m.group(2)
    return owner, repo


def detect_source(source: str, cfg: RunConfig) -> SourceSpec:
    log = get_logger()
    src = source.strip()
    if not src:
        raise ValueError("Empty source.")

    if cfg.force_github:
        if looks_like_url(src):
            url = normalize_url(src)
            gh = _detect_github_repo(url)
            if gh:
                owner, repo = gh
                return SourceSpec(source_type=SourceType.github_repo, source=src, normalized_url=url, github_owner=owner, github_repo=repo)
        raise ValueError("Forced GitHub mode but source is not a GitHub repo URL.")

    if not looks_like_url(src):
        p = Path(src).expanduser()
        if not p.exists():
            raise FileNotFoundError(f"Local path not found: {p}")
        suffix = p.suffix.lower()
        if cfg.force_pdf or suffix == ".pdf":
            return SourceSpec(source_type=SourceType.pdf_local, source=src, local_path=p)
        if cfg.force_epub or suffix == ".epub":
            return SourceSpec(source_type=SourceType.epub_local, source=src, local_path=p)
        raise ValueError("Unsupported local file type. Provide a .pdf or .epub path.")

    url = normalize_url(src)
    gh = _detect_github_repo(url)
    if gh and not cfg.force_html and not cfg.force_pdf and not cfg.force_epub:
        owner, repo = gh
        return SourceSpec(source_type=SourceType.github_repo, source=src, normalized_url=url, github_owner=owner, github_repo=repo)

    http = HttpClient.create(cfg.crawl)
    try:
        # Prefer HEAD but fall back to GET if needed
        try:
            h = http.head(url)
            ct = h.headers.get("content-type")
            status = h.status_code
        except Exception:
            ct = None
            status = 0

        if cfg.force_pdf or is_probably_pdf(ct, url):
            return SourceSpec(source_type=SourceType.pdf_url, source=src, normalized_url=url)
        if cfg.force_epub or is_probably_epub(ct, url):
            return SourceSpec(source_type=SourceType.epub_url, source=src, normalized_url=url)

        if cfg.force_html:
            return SourceSpec(source_type=SourceType.html_site, source=src, normalized_url=url)

        if status and status >= 400:
            log.warn(f"HEAD returned HTTP {status}; continuing with HTML mode.")
            return SourceSpec(source_type=SourceType.html_site, source=src, normalized_url=url)

        if is_probably_html(ct, url):
            return SourceSpec(source_type=SourceType.html_site, source=src, normalized_url=url)

        # If content-type unclear, do a small GET and sniff.
        try:
            r = http.get(url)
            ct2 = r.headers.get("content-type")
            if is_probably_pdf(ct2, url):
                return SourceSpec(source_type=SourceType.pdf_url, source=src, normalized_url=url)
            if is_probably_epub(ct2, url):
                return SourceSpec(source_type=SourceType.epub_url, source=src, normalized_url=url)
            return SourceSpec(source_type=SourceType.html_site, source=src, normalized_url=url)
        except Exception:
            return SourceSpec(source_type=SourceType.html_site, source=src, normalized_url=url)
    finally:
        http.close()


def maybe_find_github_repo_for_site(url: str, cfg: RunConfig) -> Optional[str]:
    http = HttpClient.create(cfg.crawl)
    try:
        if not http.allowed_by_robots(url):
            return None
        r = http.get(url)
        if r.status_code >= 400:
            return None
        soup = BeautifulSoup(r.text, "lxml")
        for a in soup.select("a[href]"):
            href = a.get("href")
            if not href:
                continue
            try:
                p = urlparse(href)
            except Exception:
                continue
            if p.scheme in {"http", "https"} and p.netloc.lower() == "github.com":
                gh = _detect_github_repo(href)
                if gh:
                    return f"https://github.com/{gh[0]}/{gh[1]}"
        return None
    except Exception:
        return None
    finally:
        http.close()


def run(spec: SourceSpec, cfg: RunConfig) -> RunSummary:
    from .epub_to_md import convert_epub
    from .github import pull_docs_from_repo
    from .html_crawler import crawl_site_to_markdown
    from .pdf_to_md import convert_pdf

    if cfg.output is None:
        raise ValueError("Output directory not set.")

    if spec.source_type == SourceType.github_repo:
        return pull_docs_from_repo(spec, cfg)
    if spec.source_type in {SourceType.html_site, SourceType.github_pages}:
        return crawl_site_to_markdown(spec, cfg)
    if spec.source_type in {SourceType.pdf_local, SourceType.pdf_url}:
        return convert_pdf(spec, cfg)
    if spec.source_type in {SourceType.epub_local, SourceType.epub_url}:
        return convert_epub(spec, cfg)
    raise ValueError(f"Unsupported source type: {spec.source_type}")

