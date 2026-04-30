from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import typer
from rich.prompt import Confirm, Prompt

from .detect import detect_source, maybe_find_github_repo_for_site, run
from .logging import get_logger
from .models import RunConfig, SourceType
from .output import ensure_output_dir
from .utils import looks_like_url, strip_wrapping_quotes

app = typer.Typer(add_completion=False, no_args_is_help=False)


def _interactive_config() -> RunConfig:
    log = get_logger()
    log.rule("DocHarvester")
    src = Prompt.ask("Enter a source (URL or local file path)").strip()

    cfg = RunConfig(source=src)

    if not looks_like_url(src):
        out_default = Path.cwd() / "DocHarvester Output"
    else:
        out_default = Path.cwd() / "Docs Output"

    out_str = Prompt.ask("Where should I save the docs?", default=str(out_default))
    cleaned_out = strip_wrapping_quotes(out_str)
    cfg.output = Path(cleaned_out)

    spec = detect_source(src, cfg)

    if spec.source_type == SourceType.html_site:
        if Confirm.ask("Would you like me to try to find GitHub docs for this site?", default=True):
            found = maybe_find_github_repo_for_site(spec.normalized_url or spec.source, cfg)
            if found:
                log.ok(f"Found GitHub repo: {found}")
                if Confirm.ask("Use this repo?", default=True):
                    cfg.source = found
                    cfg.force_github = True

    if not cfg.yes:
        Confirm.ask("Ready to start?", default=True, show_default=True)
    return cfg


@app.command()
def pull(
    source: Optional[str] = typer.Option(None, "--source", "-s", help="URL or local file path."),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output folder."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Assume yes for prompts."),
    github: bool = typer.Option(False, "--github", help="Force GitHub mode."),
    html: bool = typer.Option(False, "--html", help="Force HTML crawl mode."),
    pdf: bool = typer.Option(False, "--pdf", help="Force PDF conversion mode."),
    epub: bool = typer.Option(False, "--epub", help="Force EPUB conversion mode."),
    max_pages: int = typer.Option(300, "--max-pages", help="Max pages to crawl for HTML."),
    max_depth: int = typer.Option(10, "--max-depth", help="Max crawl depth for HTML."),
    delay: float = typer.Option(0.5, "--delay", help="Delay between HTTP requests (seconds)."),
    ignore_robots: bool = typer.Option(False, "--ignore-robots", help="Ignore robots.txt."),
) -> None:
    """
    Pull documentation from GitHub, HTML docs sites, PDFs, or EPUBs and export clean Markdown.
    """
    if source is None:
        cfg = _interactive_config()
    else:
        if isinstance(output, Path):
            output = Path(strip_wrapping_quotes(str(output)))
        cfg = RunConfig(
            source=source,
            output=output,
            yes=yes,
            force_github=github,
            force_html=html,
            force_pdf=pdf,
            force_epub=epub,
        )
        cfg.crawl.max_pages = max_pages
        cfg.crawl.max_depth = max_depth
        cfg.crawl.delay_seconds = delay
        cfg.crawl.respect_robots = not ignore_robots

    cfg.github_token = os.environ.get("GITHUB_TOKEN") or cfg.github_token

    if not cfg.source:
        raise typer.BadParameter("Missing --source (or run without args for interactive mode).")

    if cfg.output is None:
        cfg.output = Path.cwd() / "DocHarvester Output"

    out_dir = ensure_output_dir(cfg.output)
    cfg.output = out_dir

    spec = detect_source(cfg.source, cfg)
    summary = run(spec, cfg)

    log = get_logger()
    log.rule("Summary")
    log.info(f"Source type: {summary.source_type.value}")
    log.info(f"Processed: {summary.processed_count}")
    if summary.skipped_count:
        log.warn(f"Skipped: {summary.skipped_count}")
    log.ok(f"Output: {summary.output_dir}")
    for w in summary.warnings:
        log.warn(w)


@app.callback(invoke_without_command=True)
def _main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        # NOTE: ctx.invoke(pull) passes Typer OptionInfo defaults to pull(), which breaks pydantic validation.
        # We call interactive mode directly to avoid Click/Typer default injection.
        cfg = _interactive_config()
        spec = detect_source(cfg.source or "", cfg)
        summary = run(spec, cfg)

        log = get_logger()
        log.rule("Summary")
        log.info(f"Source type: {summary.source_type.value}")
        log.info(f"Processed: {summary.processed_count}")
        if summary.skipped_count:
            log.warn(f"Skipped: {summary.skipped_count}")
        log.ok(f"Output: {summary.output_dir}")
        for w in summary.warnings:
            log.warn(w)

