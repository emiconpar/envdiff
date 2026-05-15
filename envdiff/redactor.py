"""Redactor module: mask sensitive environment variable values."""

import re
from typing import Dict, List, Optional

_DEFAULT_PATTERNS: List[str] = [
    r"(?i)password",
    r"(?i)secret",
    r"(?i)token",
    r"(?i)api[_]?key",
    r"(?i)private[_]?key",
    r"(?i)auth",
    r"(?i)credential",
]

DEFAULT_MASK = "***REDACTED***"


def _is_sensitive(key: str, patterns: List[str]) -> bool:
    """Return True if the key matches any of the given regex patterns."""
    return any(re.search(pattern, key) for pattern in patterns)


def redact_env(
    env: Dict[str, str],
    patterns: Optional[List[str]] = None,
    mask: str = DEFAULT_MASK,
) -> Dict[str, str]:
    """Return a copy of env with sensitive values replaced by mask."""
    if patterns is None:
        patterns = _DEFAULT_PATTERNS
    return {
        key: (mask if _is_sensitive(key, patterns) else value)
        for key, value in env.items()
    }


def redact_keys(
    env: Dict[str, str],
    keys: List[str],
    mask: str = DEFAULT_MASK,
) -> Dict[str, str]:
    """Return a copy of env with specific keys masked."""
    key_set = set(keys)
    return {
        key: (mask if key in key_set else value)
        for key, value in env.items()
    }


def sensitive_keys(
    env: Dict[str, str],
    patterns: Optional[List[str]] = None,
) -> List[str]:
    """Return a list of keys in env that are considered sensitive."""
    if patterns is None:
        patterns = _DEFAULT_PATTERNS
    return [key for key in env if _is_sensitive(key, patterns)]
