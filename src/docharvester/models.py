from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class SourceType(str, Enum):
    github_repo = "github_repo"
    github_pages = "github_pages"
    html_site = "html_site"
    pdf_local = "pdf_local"
    pdf_url = "pdf_url"
    epub_local = "epub_local"
    epub_url = "epub_url"


class SourceSpec(BaseModel):
    source_type: SourceType
    source: str
    normalized_url: Optional[str] = None
    local_path: Optional[Path] = None

    github_owner: Optional[str] = None
    github_repo: Optional[str] = None
    github_ref: Optional[str] = None

    title_hint: Optional[str] = None


class CrawlConfig(BaseModel):
    max_pages: int = Field(default=300, ge=1)
    max_depth: int = Field(default=10, ge=0)
    delay_seconds: float = Field(default=0.5, ge=0.0)
    respect_robots: bool = True
    same_origin_only: bool = True


class RunConfig(BaseModel):
    source: Optional[str] = None
    output: Optional[Path] = None
    yes: bool = False

    force_github: bool = False
    force_html: bool = False
    force_pdf: bool = False
    force_epub: bool = False

    crawl: CrawlConfig = Field(default_factory=CrawlConfig)
    github_token: Optional[str] = None


class RunSummary(BaseModel):
    source_type: SourceType
    output_dir: Path
    processed_count: int = 0
    skipped_count: int = 0
    warnings: list[str] = Field(default_factory=list)
    skipped: list[str] = Field(default_factory=list)

