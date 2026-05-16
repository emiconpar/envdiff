"""Formatting helpers for stringer output reports."""
from __future__ import annotations

from typing import Dict


def _bold(text: str, color: bool = True) -> str:
    return f"\033[1m{text}\033[0m" if color else text


def _cyan(text: str, color: bool = True) -> str:
    return f"\033[36m{text}\033[0m" if color else text


def _dim(text: str, color: bool = True) -> str:
    return f"\033[2m{text}\033[0m" if color else text


def format_dotenv_report(
    env: Dict[str, str],
    label: str = "env",
    sort: bool = False,
    export: bool = False,
    color: bool = True,
) -> str:
    """Return a formatted report showing the .env rendering of an env dict."""
    from envdiff.stringer import to_dotenv

    header = _bold(_cyan(f"=== {label} (.env format) ===", color), color)
    body = to_dotenv(env, sort=sort, export=export)
    if not body:
        body = _dim("(empty)", color)
    return f"{header}\n{body}"


def format_inline_report(
    env: Dict[str, str],
    label: str = "env",
    separator: str = " ",
    sort: bool = False,
    color: bool = True,
) -> str:
    """Return a formatted report showing the inline rendering of an env dict."""
    from envdiff.stringer import to_inline

    header = _bold(_cyan(f"=== {label} (inline) ===", color), color)
    body = to_inline(env, separator=separator, sort=sort)
    if not body:
        body = _dim("(empty)", color)
    return f"{header}\n{body}"


def stringer_summary(env: Dict[str, str], label: str = "env") -> str:
    """One-line summary of how many keys would be rendered."""
    count = len(env)
    return f"{label}: {count} key(s) ready for rendering"
