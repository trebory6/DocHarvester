from __future__ import annotations

import fnmatch
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import httpx

from .logging import get_logger
from .md_clean import simplify_mdx_to_md
from .models import RunConfig, RunSummary, SourceSpec, SourceType
from .output import IndexItem, make_project_dir, prepend_frontmatter, write_index
from .utils import ensure_dir, relpath_posix, safe_filename


_DOCS_ROOT_PATTERNS = [
    "docs",
    "doc",
    "documentation",
    "website/docs",
    "packages/*/docs",
    "apps/*/docs",
]

_IGNORE_DIRS = {
    "node_modules",
    "dist",
    "build",
    ".git",
    ".github",
    ".next",
    ".cache",
    ".docusaurus",
    ".vitepress",
}


@dataclass(frozen=True)
class GithubRepo:
    owner: str
    repo: str
    default_branch: str


def _github_headers(token: Optional[str]) -> dict[str, str]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "DocHarvester/0.1",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _get_default_branch(owner: str, repo: str, token: Optional[str]) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}"
    r = httpx.get(url, headers=_github_headers(token), timeout=30.0, follow_redirects=True)
    if r.status_code == 403:
        raise RuntimeError(
            "GitHub API rate limit hit (HTTP 403). Set GITHUB_TOKEN env var to increase limits."
        )
    r.raise_for_status()
    data = r.json()
    return data.get("default_branch") or "main"


def _list_tree(owner: str, repo: str, branch: str, token: Optional[str]) -> list[dict]:
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    r = httpx.get(url, headers=_github_headers(token), timeout=60.0, follow_redirects=True)
    if r.status_code == 403:
        raise RuntimeError(
            "GitHub API rate limit hit (HTTP 403). Set GITHUB_TOKEN env var to increase limits."
        )
    r.raise_for_status()
    data = r.json()
    return data.get("tree") or []


def _is_ignored_path(path: str) -> bool:
    parts = path.split("/")
    return any(p in _IGNORE_DIRS or p.startswith(".") and p not in {".well-known"} for p in parts)


def _score_doc_path(path: str) -> int:
    path_norm = path.strip("/")
    if not path_norm:
        return 0
    folder = "/".join(path_norm.split("/")[:-1])
    score = 0
    for pat in _DOCS_ROOT_PATTERNS:
        if fnmatch.fnmatch(folder, pat) or folder.startswith(pat + "/") or folder == pat:
            score += 10
    if folder.startswith("docs/") or folder == "docs":
        score += 5
    return score


def _filter_doc_files(tree: Iterable[dict]) -> list[str]:
    out: list[str] = []
    for item in tree:
        if item.get("type") != "blob":
            continue
        path = item.get("path") or ""
        if not path:
            continue
        if _is_ignored_path(path):
            continue
        lower = path.lower()
        if lower.endswith((".md", ".mdx")):
            out.append(path)
    return out


def _download_raw(owner: str, repo: str, branch: str, path: str, token: Optional[str]) -> str:
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
    headers: dict[str, str] = {"User-Agent": "DocHarvester/0.1"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = httpx.get(raw_url, headers=headers, timeout=60.0, follow_redirects=True)
    r.raise_for_status()
    return r.text


def _write_doc_file(out_root: Path, rel_path: str, content: str) -> Path:
    rel = Path(rel_path)
    target = out_root / rel
    ensure_dir(target.parent)
    target.write_text(content, encoding="utf-8")
    return target


def pull_docs_from_repo(spec: SourceSpec, cfg: RunConfig) -> RunSummary:
    log = get_logger()
    if not spec.github_owner or not spec.github_repo:
        raise ValueError("Missing GitHub owner/repo in source spec.")
    owner, repo = spec.github_owner, spec.github_repo

    token = cfg.github_token or os.environ.get("GITHUB_TOKEN")
    branch = _get_default_branch(owner, repo, token)
    gh = GithubRepo(owner=owner, repo=repo, default_branch=branch)

    project_name = safe_filename(f"{gh.repo} Docs")
    out_dir = make_project_dir(cfg.output or Path.cwd(), project_name)

    log.rule(f"GitHub: {owner}/{repo} ({branch})")
    tree = _list_tree(owner, repo, branch, token)
    candidates = _filter_doc_files(tree)
    if not candidates:
        summary = RunSummary(source_type=SourceType.github_repo, output_dir=out_dir)
        summary.warnings.append("No .md/.mdx files found in repo tree. Try HTML crawl mode instead.")
        return summary

    # Sort by docs-root score, then path depth.
    candidates.sort(key=lambda p: (-_score_doc_path(p), p.count("/"), p))

    written: list[IndexItem] = []
    summary = RunSummary(source_type=SourceType.github_repo, output_dir=out_dir)
    repo_url = f"https://github.com/{owner}/{repo}"

    for path in candidates:
        try:
            text = _download_raw(owner, repo, branch, path, token)
            if path.lower().endswith(".mdx"):
                text = simplify_mdx_to_md(text)
                out_path = str(Path(path).with_suffix(".md").as_posix())
            else:
                out_path = path
            page_name = Path(out_path).stem
            text = prepend_frontmatter(
                text,
                {
                    "page_name": page_name,
                    "source_url": repo_url,
                    "pull_type": "github",
                },
            )
            saved = _write_doc_file(out_dir, out_path, text)
            written.append(IndexItem(title=Path(out_path).stem, md_path=saved))
            summary.processed_count += 1
        except Exception as e:
            summary.skipped_count += 1
            summary.skipped.append(path)
            summary.warnings.append(f"Skipped {path}: {e}")

    write_index(out_dir, f"{gh.repo} Docs", written)
    log.ok(f"Downloaded {summary.processed_count} files.")
    return summary

