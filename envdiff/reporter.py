"""Generate human-readable merge reports."""

from typing import Dict, List, Optional
from envdiff.merger import merge_conflicts


def conflict_report(
    envs: List[Dict[str, str]],
    labels: Optional[List[str]] = None,
    use_color: bool = False,
) -> str:
    """Return a formatted string describing all merge conflicts.

    Args:
        envs: List of env dicts to inspect.
        labels: Human-readable names for each env dict.
        use_color: If True, use ANSI color codes.

    Returns:
        Multi-line report string.
    """
    labels = labels or [f"env[{i}]" for i in range(len(envs))]
    conflicts = merge_conflicts(envs)

    if not conflicts:
        msg = "No conflicts found."
        return _green(msg) if use_color else msg

    lines: List[str] = []
    header = f"{len(conflicts)} conflict(s) detected:"
    lines.append(_yellow(header) if use_color else header)
    lines.append("")

    for key in sorted(conflicts):
        key_line = f"  {key}:"
        lines.append(_bold(key_line) if use_color else key_line)
        for env, label in zip(envs, labels):
            if key in env:
                val_line = f"    [{label}] {env[key]}"
                lines.append(_red(val_line) if use_color else val_line)

    return "\n".join(lines)


def merge_summary(
    envs: List[Dict[str, str]],
    labels: Optional[List[str]] = None,
) -> Dict[str, int]:
    """Return counts of total keys, unique keys, and conflicting keys."""
    labels = labels or [f"env[{i}]" for i in range(len(envs))]
    all_keys = set()
    for env in envs:
        all_keys.update(env.keys())

    conflicts = merge_conflicts(envs)
    return {
        "total_keys": len(all_keys),
        "conflict_keys": len(conflicts),
        "clean_keys": len(all_keys) - len(conflicts),
    }


def _red(s: str) -> str:
    return f"\033[31m{s}\033[0m"


def _green(s: str) -> str:
    return f"\033[32m{s}\033[0m"


def _yellow(s: str) -> str:
    return f"\033[33m{s}\033[0m"


def _bold(s: str) -> str:
    return f"\033[1m{s}\033[0m"
