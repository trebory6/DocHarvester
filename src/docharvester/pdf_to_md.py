from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import fitz  # PyMuPDF
import httpx

from .logging import get_logger
from .models import RunConfig, RunSummary, SourceSpec, SourceType
from .output import IndexItem, make_project_dir, prepend_frontmatter, write_index
from .utils import ensure_dir, safe_filename


@dataclass(frozen=True)
class PdfExtractStats:
    pages: int
    total_chars: int
    pages_with_text: int


def _download_pdf(url: str, dest: Path) -> Path:
    r = httpx.get(url, timeout=120.0, follow_redirects=True)
    r.raise_for_status()
    dest.write_bytes(r.content)
    return dest


def _reflow_text(text: str) -> str:
    # Merge wrapped lines into paragraphs, preserve blank lines as paragraph breaks.
    lines = [ln.rstrip() for ln in text.splitlines()]
    out: list[str] = []
    buf: list[str] = []

    def flush() -> None:
        nonlocal buf
        if not buf:
            return
        joined = " ".join(x.strip() for x in buf if x.strip())
        if joined:
            out.append(joined)
        buf = []

    for ln in lines:
        if not ln.strip():
            flush()
            out.append("")
            continue
        # If line looks like a hyphenated wrap, join without hyphen.
        if ln.endswith("-") and len(ln) > 3 and not ln.endswith(" -"):
            buf.append(ln[:-1])
        else:
            buf.append(ln)
    flush()

    # Remove excess blank lines
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out).strip() + "\n"


def _extract_pdf_to_markdown(pdf_path: Path) -> tuple[str, PdfExtractStats]:
    doc = fitz.open(pdf_path)
    pages = doc.page_count
    chunks: list[str] = []
    total_chars = 0
    pages_with_text = 0

    for i in range(pages):
        page = doc.load_page(i)
        text = page.get_text("text") or ""
        if text.strip():
            pages_with_text += 1
        total_chars += len(text)
        chunks.append(text)

    doc.close()

    md_parts: list[str] = []
    for i, raw in enumerate(chunks, start=1):
        raw = raw.strip("\n")
        if not raw.strip():
            continue
        md_parts.append(f"## Page {i}\n")
        md_parts.append(_reflow_text(raw))
        md_parts.append("")

    md = "\n".join(md_parts).strip() + "\n"
    return md, PdfExtractStats(pages=pages, total_chars=total_chars, pages_with_text=pages_with_text)


def _likely_scanned(stats: PdfExtractStats) -> bool:
    if stats.pages == 0:
        return False
    if stats.pages_with_text == 0:
        return True
    avg = stats.total_chars / max(stats.pages, 1)
    # Heuristic: if very low text per page, extraction quality likely poor.
    return avg < 200


def convert_pdf(spec: SourceSpec, cfg: RunConfig) -> RunSummary:
    log = get_logger()
    out_parent = cfg.output or Path.cwd()

    if spec.source_type == SourceType.pdf_local:
        pdf_path = Path(spec.local_path or "")
        name = safe_filename(pdf_path.stem)
    elif spec.source_type == SourceType.pdf_url:
        url = spec.normalized_url or spec.source
        name = safe_filename(Path(urlparse(url).path).stem or "document")
        pdf_path = Path("")
    else:
        raise ValueError(f"Unsupported PDF spec: {spec.source_type}")

    out_dir = make_project_dir(out_parent, f"{name} PDF")
    summary = RunSummary(source_type=spec.source_type, output_dir=out_dir)
    if spec.source_type == SourceType.pdf_url:
        url = spec.normalized_url or spec.source
        pdf_path = out_dir / f"{name}.pdf"
        _download_pdf(url, pdf_path)

    try:
        md, stats = _extract_pdf_to_markdown(pdf_path)
        md = prepend_frontmatter(
            md,
            {
                "page_name": name,
                "source_url": pdf_path.name,
                "pull_type": "pdf",
            },
        )
        md_path = out_dir / f"{safe_filename(name)}.md"
        md_path.write_text(md, encoding="utf-8")
        summary.processed_count = 1

        if _likely_scanned(stats):
            summary.warnings.append(
                "PDF text extraction looks weak (may be scanned). OCR may be required for better results."
            )

        write_index(out_dir, f"{name} PDF", [IndexItem(title=name, md_path=md_path)])
        log.ok(f"Converted PDF to {md_path.name}")
        return summary
    except Exception as e:
        summary.warnings.append(f"PDF conversion failed: {e}")
        return summary

