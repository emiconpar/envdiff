"""Reporting utilities for variable interpolation results."""

from typing import Dict, List


def _yellow(text: str) -> str:
    return f"\033[33m{text}\033[0m"


def _green(text: str) -> str:
    return f"\033[32m{text}\033[0m"


def _red(text: str) -> str:
    return f"\033[31m{text}\033[0m"


def format_interpolation_report(
    original: Dict[str, str],
    interpolated: Dict[str, str],
    unresolved: Dict[str, List[str]],
    label: str = "env",
    color: bool = True,
) -> str:
    """Format a human-readable report of interpolation changes.

    Args:
        original: The environment before interpolation.
        interpolated: The environment after interpolation.
        unresolved: Mapping of keys to lists of unresolved variable names.
        label: A label to identify the environment in the report.
        color: Whether to use ANSI color codes.

    Returns:
        A formatted string report.
    """
    lines: List[str] = [f"Interpolation report for [{label}]"]
    changed = [
        k for k in original if original[k] != interpolated.get(k)
    ]

    if changed:
        lines.append(f"  Resolved ({len(changed)}):")
        for key in sorted(changed):
            before = original[key]
            after = interpolated[key]
            entry = f"    {key}: {before!r} -> {after!r}"
            lines.append(_green(entry) if color else entry)
    else:
        ok = "  No substitutions made."
        lines.append(_green(ok) if color else ok)

    if unresolved:
        lines.append(f"  Unresolved references ({len(unresolved)}):")
        for key, refs in sorted(unresolved.items()):
            entry = f"    {key}: missing {refs}"
            lines.append(_yellow(entry) if color else entry)

    return "\n".join(lines)


def interpolation_summary(unresolved: Dict[str, List[str]], color: bool = True) -> str:
    """Return a one-line summary of unresolved references."""
    if not unresolved:
        msg = "All references resolved."
        return _green(msg) if color else msg
    count = sum(len(v) for v in unresolved.values())
    msg = f"{count} unresolved reference(s) in {len(unresolved)} key(s)."
    return _red(msg) if color else msg
