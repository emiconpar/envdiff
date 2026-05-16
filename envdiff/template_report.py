"""Human-readable reports for env template rendering results."""

from __future__ import annotations

from typing import Dict, Optional


def _green(text: str, color: bool = True) -> str:
    return f"\033[32m{text}\033[0m" if color else text


def _yellow(text: str, color: bool = True) -> str:
    return f"\033[33m{text}\033[0m" if color else text


def _bold(text: str, color: bool = True) -> str:
    return f"\033[1m{text}\033[0m" if color else text


def format_template_report(
    summary: Dict[str, object],
    color: bool = True,
) -> str:
    """Format a template rendering summary as a multi-line string."""
    lines: list[str] = []
    label = summary.get("label", "env")
    lines.append(_bold(f"Template Report: {label}", color))
    lines.append(f"  Total keys     : {summary['total']}")
    lines.append(
        f"  Rendered       : "
        + _green(str(summary["rendered_count"]), color)
    )

    unrendered_count = int(str(summary["unrendered_count"]))
    unrendered_label = _yellow(str(unrendered_count), color) if unrendered_count else str(unrendered_count)
    lines.append(f"  Unrendered     : {unrendered_label}")

    rendered_keys = summary.get("rendered_keys", [])
    if rendered_keys:
        lines.append("  Rendered keys  :")
        for key in rendered_keys:  # type: ignore[union-attr]
            lines.append(f"    {_green('+', color)} {key}")

    unrendered_keys = summary.get("unrendered_keys", [])
    if unrendered_keys:
        lines.append("  Unrendered keys:")
        for key in unrendered_keys:  # type: ignore[union-attr]
            lines.append(f"    {_yellow('?', color)} {key}")

    return "\n".join(lines)


def template_summary_line(
    summary: Dict[str, object],
    color: bool = True,
) -> str:
    """Return a compact one-line summary suitable for CLI output."""
    label = summary.get("label", "env")
    rendered = summary["rendered_count"]
    unrendered = summary["unrendered_count"]
    parts = [f"{label}: {rendered} rendered"]
    if unrendered:
        parts.append(_yellow(f"{unrendered} unrendered", color))
    else:
        parts.append(_green("all resolved", color))
    return ", ".join(parts)
