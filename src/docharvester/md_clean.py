from __future__ import annotations

import re


_MDX_IMPORT_EXPORT_RE = re.compile(r"^\s*(import|export)\s.+$", re.MULTILINE)
_JSX_BLOCK_RE = re.compile(r"^\s*<([A-Z][A-Za-z0-9_]*)[\s\S]*?^\s*</\1>\s*$", re.MULTILINE)
_JSX_SELF_CLOSING_RE = re.compile(r"^\s*<([A-Z][A-Za-z0-9_]*)(\s+[^>]*)?/>\s*$", re.MULTILINE)


def simplify_mdx_to_md(text: str) -> str:
    """
    Best-effort MDX -> Markdown simplification for docs exports.
    Keeps Markdown + code fences, strips most JSX and import/export lines.
    """
    out = text
    out = _MDX_IMPORT_EXPORT_RE.sub("", out)

    # Remove large JSX blocks (custom components). This is conservative and avoids touching inline HTML.
    out = _JSX_BLOCK_RE.sub("", out)
    out = _JSX_SELF_CLOSING_RE.sub("", out)

    # Collapse multiple blank lines.
    out = re.sub(r"\n{4,}", "\n\n\n", out)
    return out.strip() + "\n"

