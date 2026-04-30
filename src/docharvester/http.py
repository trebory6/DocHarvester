from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import httpx

from .models import CrawlConfig
from .utils import normalize_url, strip_fragment


@dataclass
class HttpClient:
    client: httpx.Client
    cfg: CrawlConfig
    _robots_cache: dict[str, RobotFileParser]
    _last_request_time: float = 0.0

    @classmethod
    def create(cls, cfg: CrawlConfig) -> "HttpClient":
        headers = {
            "User-Agent": "DocHarvester/0.1 (+https://example.invalid)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
        client = httpx.Client(
            headers=headers,
            follow_redirects=True,
            timeout=httpx.Timeout(30.0),
        )
        return cls(client=client, cfg=cfg, _robots_cache={})

    def close(self) -> None:
        self.client.close()

    def _sleep_if_needed(self) -> None:
        delay = self.cfg.delay_seconds
        if delay <= 0:
            return
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < delay:
            time.sleep(delay - elapsed)

    def _mark_request(self) -> None:
        self._last_request_time = time.time()

    def _robots_for(self, url: str) -> RobotFileParser:
        p = urlparse(url)
        origin = f"{p.scheme}://{p.netloc}"
        if origin in self._robots_cache:
            return self._robots_cache[origin]
        robots_url = urljoin(origin, "/robots.txt")
        rp = RobotFileParser()
        rp.set_url(robots_url)
        try:
            self._sleep_if_needed()
            r = self.client.get(robots_url)
            self._mark_request()
            if r.status_code < 400:
                rp.parse(r.text.splitlines())
            else:
                rp.parse([])
        except Exception:
            rp.parse([])
        self._robots_cache[origin] = rp
        return rp

    def allowed_by_robots(self, url: str) -> bool:
        if not self.cfg.respect_robots:
            return True
        rp = self._robots_for(url)
        return rp.can_fetch(self.client.headers.get("User-Agent", "*"), url)

    def head(self, url: str) -> httpx.Response:
        self._sleep_if_needed()
        r = self.client.head(url)
        self._mark_request()
        return r

    def get(self, url: str) -> httpx.Response:
        self._sleep_if_needed()
        r = self.client.get(url)
        self._mark_request()
        return r


def is_probably_html(content_type: Optional[str], url: str) -> bool:
    ct = (content_type or "").lower()
    if "text/html" in ct or "application/xhtml" in ct:
        return True
    path = urlparse(url).path.lower()
    if path.endswith((".html", ".htm", "/")):
        return True
    return False


def is_probably_pdf(content_type: Optional[str], url: str) -> bool:
    ct = (content_type or "").lower()
    if "application/pdf" in ct:
        return True
    return urlparse(url).path.lower().endswith(".pdf")


def is_probably_epub(content_type: Optional[str], url: str) -> bool:
    ct = (content_type or "").lower()
    if "application/epub+zip" in ct:
        return True
    return urlparse(url).path.lower().endswith(".epub")


def canonicalize_url(url: str) -> str:
    url = normalize_url(url)
    url = strip_fragment(url)
    p = urlparse(url)
    path = p.path or "/"
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return p._replace(path=path).geturl()

