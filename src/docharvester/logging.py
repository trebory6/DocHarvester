from __future__ import annotations

import os
from dataclasses import dataclass

from rich.console import Console
from rich.theme import Theme


@dataclass(frozen=True)
class Log:
    console: Console

    def info(self, msg: str) -> None:
        self.console.print(f"[info]{msg}[/info]")

    def ok(self, msg: str) -> None:
        self.console.print(f"[ok]{msg}[/ok]")

    def warn(self, msg: str) -> None:
        self.console.print(f"[warn]{msg}[/warn]")

    def error(self, msg: str) -> None:
        self.console.print(f"[error]{msg}[/error]")

    def rule(self, title: str) -> None:
        self.console.rule(title)


def get_logger() -> Log:
    theme = Theme(
        {
            "info": "cyan",
            "ok": "green",
            "warn": "yellow",
            "error": "bold red",
        }
    )
    force_terminal = None
    if os.environ.get("CI"):
        force_terminal = True
    console = Console(theme=theme, force_terminal=force_terminal)
    return Log(console=console)

