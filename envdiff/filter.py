"""Filtering utilities for environment variable sets."""

from __future__ import annotations

import fnmatch
import re
from typing import Dict, List, Optional


def filter_by_prefix(
    env: Dict[str, str], prefixes: List[str], exclude: bool = False
) -> Dict[str, str]:
    """Return entries whose keys start with any of the given prefixes.

    Args:
        env: Source environment mapping.
        prefixes: List of prefix strings to match against.
        exclude: When True, *exclude* matching keys instead of keeping them.

    Returns:
        Filtered copy of *env*.
    """
    result: Dict[str, str] = {}
    for key, value in env.items():
        matches = any(key.startswith(p) for p in prefixes)
        if matches != exclude:
            result[key] = value
    return result


def filter_by_pattern(
    env: Dict[str, str], pattern: str, exclude: bool = False
) -> Dict[str, str]:
    """Return entries whose keys match a shell-style glob *pattern*.

    Args:
        env: Source environment mapping.
        pattern: Glob pattern (e.g. ``'AWS_*'``).
        exclude: When True, *exclude* matching keys instead of keeping them.

    Returns:
        Filtered copy of *env*.
    """
    result: Dict[str, str] = {}
    for key, value in env.items():
        matches = fnmatch.fnmatchcase(key, pattern)
        if matches != exclude:
            result[key] = value
    return result


def filter_by_regex(
    env: Dict[str, str], regex: str, exclude: bool = False
) -> Dict[str, str]:
    """Return entries whose keys match a regular expression.

    Args:
        env: Source environment mapping.
        regex: Regular expression string applied to each key.
        exclude: When True, *exclude* matching keys instead of keeping them.

    Returns:
        Filtered copy of *env*.

    Raises:
        re.error: If *regex* is not a valid regular expression.
    """
    compiled = re.compile(regex)
    result: Dict[str, str] = {}
    for key, value in env.items():
        matches = compiled.search(key) is not None
        if matches != exclude:
            result[key] = value
    return result


def select_keys(
    env: Dict[str, str], keys: List[str]
) -> Dict[str, str]:
    """Return only the specified *keys* from *env* (missing keys are ignored)."""
    return {k: env[k] for k in keys if k in env}
