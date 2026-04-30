from __future__ import annotations

import hashlib
import re
import unicodedata
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import urlparse, urlunparse


def looks_like_url(s: str) -> bool:
    try:
        p = urlparse(s)
    except Exception:
        return False
    return p.scheme in {"http", "https"} and bool(p.netloc)


def normalize_url(url: str) -> str:
    p = urlparse(url)
    scheme = p.scheme.lower()
    netloc = p.netloc.lower()
    path = p.path or "/"
    return urlunparse((scheme, netloc, path, "", p.query, ""))


def strip_fragment(url: str) -> str:
    p = urlparse(url)
    return urlunparse((p.scheme, p.netloc, p.path, p.params, p.query, ""))


def safe_filename(name: str, max_len: int = 120) -> str:
    name = unicodedata.normalize("NFKC", name)
    name = name.replace("\n", " ").replace("\r", " ").strip()
    name = re.sub(r"\s+", " ", name)
    name = re.sub(r'[<>:"/\\\\|?*]+', "-", name)
    name = name.strip(" .-_")
    if not name:
        name = "output"
    if len(name) > max_len:
        name = name[:max_len].rstrip(" .-_")
    return name


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def guess_name_from_url(url: str) -> str:
    p = urlparse(url)
    host = p.netloc.split(":")[0]
    path = p.path.strip("/")
    if not path:
        return safe_filename(host)
    tail = path.split("/")[-1]
    if tail.lower() in {"index.html", "index"} and len(path.split("/")) > 1:
        tail = path.split("/")[-2]
    return safe_filename(f"{host} {tail}")


def relpath_posix(path: Path, start: Path) -> str:
    return path.relative_to(start).as_posix()


def pick_first(items: Iterable[Optional[str]]) -> Optional[str]:
    for x in items:
        if x:
            return x
    return None


def strip_wrapping_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        return s[1:-1].strip()
    return s

