"""Human-readable reports for patch operations."""

from typing import Dict
from envdiff.patcher import patch_summary
from envdiff.diff import EnvDiffResult


def _green(text: str, color: bool) -> str:
    return f"\033[32m{text}\033[0m" if color else text


def _red(text: str, color: bool) -> str:
    return f"\033[31m{text}\033[0m" if color else text


def _yellow(text: str, color: bool) -> str:
    return f"\033[33m{text}\033[0m" if color else text


def _bold(text: str, color: bool) -> str:
    return f"\033[1m{text}\033[0m" if color else text


def format_patch_report(
    diff: EnvDiffResult,
    label: str = "patch",
    color: bool = True,
) -> str:
    """Return a multi-line string describing what the patch will do."""
    lines = [_bold(f"Patch report [{label}]", color)]

    for key, value in diff.only_in_right.items():
        lines.append("  " + _green(f"+ {key}={value}", color))

    for key in diff.only_in_left:
        lines.append("  " + _red(f"- {key}", color))

    for key, (left_val, right_val) in diff.changed.items():
        lines.append(
            "  "
            + _yellow(f"~ {key}: {left_val!r} -> {right_val!r}", color)
        )

    if not diff.only_in_right and not diff.only_in_left and not diff.changed:
        lines.append("  " + _green("No changes — patch is a no-op.", color))

    return "\n".join(lines)


def patch_summary_line(
    diff: EnvDiffResult,
    color: bool = True,
) -> str:
    """Return a single-line summary of patch statistics."""
    counts = patch_summary(diff)
    parts = [
        _green(f"+{counts['additions']} added", color),
        _red(f"-{counts['deletions']} removed", color),
        _yellow(f"~{counts['modifications']} modified", color),
    ]
    return "Patch: " + ", ".join(parts)
