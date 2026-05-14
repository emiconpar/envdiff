"""Formatting utilities for displaying environment variable diffs."""

from typing import Optional
from .diff import EnvDiffResult


ANSI_RED = "\033[91m"
ANSI_GREEN = "\033[92m"
ANSI_YELLOW = "\033[93m"
ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"


def _colorize(text: str, color: str, use_color: bool = True) -> str:
    if not use_color:
        return text
    return f"{color}{text}{ANSI_RESET}"


def format_diff(
    result: EnvDiffResult,
    left_label: str = "left",
    right_label: str = "right",
    use_color: bool = True,
    show_unchanged: bool = False,
) -> str:
    """Format an EnvDiffResult into a human-readable string."""
    lines = []

    header = f"--- {left_label}\n+++ {right_label}"
    lines.append(_colorize(header, ANSI_BOLD, use_color))
    lines.append("")

    if result.only_in_left:
        lines.append(_colorize(f"Only in {left_label}:", ANSI_BOLD, use_color))
        for key in sorted(result.only_in_left):
            value = result.only_in_left[key]
            lines.append(_colorize(f"  - {key}={value}", ANSI_RED, use_color))
        lines.append("")

    if result.only_in_right:
        lines.append(_colorize(f"Only in {right_label}:", ANSI_BOLD, use_color))
        for key in sorted(result.only_in_right):
            value = result.only_in_right[key]
            lines.append(_colorize(f"  + {key}={value}", ANSI_GREEN, use_color))
        lines.append("")

    if result.changed:
        lines.append(_colorize("Changed values:", ANSI_BOLD, use_color))
        for key in sorted(result.changed):
            old_val, new_val = result.changed[key]
            lines.append(_colorize(f"  - {key}={old_val}", ANSI_RED, use_color))
            lines.append(_colorize(f"  + {key}={new_val}", ANSI_GREEN, use_color))
        lines.append("")

    if show_unchanged and result.unchanged:
        lines.append(_colorize("Unchanged:", ANSI_BOLD, use_color))
        for key in sorted(result.unchanged):
            lines.append(f"    {key}={result.unchanged[key]}")
        lines.append("")

    if not result.only_in_left and not result.only_in_right and not result.changed:
        lines.append(_colorize("No differences found.", ANSI_GREEN, use_color))

    return "\n".join(lines).rstrip()


def format_summary(result: EnvDiffResult, use_color: bool = True) -> str:
    """Format a one-line summary of the diff result."""
    parts = []
    if result.only_in_left:
        parts.append(_colorize(f"{len(result.only_in_left)} removed", ANSI_RED, use_color))
    if result.only_in_right:
        parts.append(_colorize(f"{len(result.only_in_right)} added", ANSI_GREEN, use_color))
    if result.changed:
        parts.append(_colorize(f"{len(result.changed)} changed", ANSI_YELLOW, use_color))
    if not parts:
        return _colorize("No differences.", ANSI_GREEN, use_color)
    return ", ".join(parts) + "."
