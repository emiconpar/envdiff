"""Redaction report: summarise which keys were redacted in an env dict."""

from typing import Dict, List, Optional

from envdiff.redactor import sensitive_keys, DEFAULT_MASK


def _yellow(text: str) -> str:
    return f"\033[33m{text}\033[0m"


def _green(text: str) -> str:
    return f"\033[32m{text}\033[0m"


def format_redaction_report(
    env: Dict[str, str],
    patterns: Optional[List[str]] = None,
    label: str = "env",
    color: bool = True,
) -> str:
    """Return a human-readable report of sensitive keys found in env."""
    found = sensitive_keys(env, patterns=patterns)
    lines: List[str] = []
    header = f"Redaction report for [{label}]"
    lines.append(header)
    lines.append("-" * len(header))

    if not found:
        msg = "No sensitive keys detected."
        lines.append(_green(msg) if color else msg)
    else:
        for key in sorted(found):
            entry = f"  {key}: {DEFAULT_MASK}"
            lines.append(_yellow(entry) if color else entry)

    return "\n".join(lines)


def redaction_summary(
    env: Dict[str, str],
    patterns: Optional[List[str]] = None,
) -> Dict[str, int]:
    """Return a summary dict with total keys and count of sensitive ones."""
    found = sensitive_keys(env, patterns=patterns)
    return {
        "total_keys": len(env),
        "sensitive_keys": len(found),
        "clean_keys": len(env) - len(found),
    }
