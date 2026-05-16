"""Formatting helpers for masker output."""

from __future__ import annotations

from envdiff.masker import mask_summary


def _yellow(text: str, color: bool = True) -> str:
    return f"\033[33m{text}\033[0m" if color else text


def _green(text: str, color: bool = True) -> str:
    return f"\033[32m{text}\033[0m" if color else text


def _bold(text: str, color: bool = True) -> str:
    return f"\033[1m{text}\033[0m" if color else text


def format_mask_report(
    masked_env: dict[str, str],
    original_env: dict[str, str],
    label: str = "env",
    color: bool = True,
) -> str:
    """Return a human-readable report of which keys were masked."""
    summary = mask_summary(masked_env, original_env)
    lines: list[str] = []
    lines.append(_bold(f"Mask report: {label}", color))
    lines.append(f"  Total keys : {summary['total_keys']}")
    masked_count = summary["masked_count"]
    if masked_count == 0:
        lines.append(_green("  No keys masked.", color))
    else:
        lines.append(_yellow(f"  Masked keys: {masked_count}", color))
        for key in summary["masked_keys"]:
            lines.append(f"    - {key}: {masked_env[key]}")
    return "\n".join(lines)


def masking_summary(masked_env: dict[str, str], original_env: dict[str, str]) -> str:
    """Return a one-line summary string."""
    summary = mask_summary(masked_env, original_env)
    count = summary["masked_count"]
    total = summary["total_keys"]
    if count == 0:
        return f"No keys masked ({total} total)."
    return f"{count}/{total} key(s) masked."
