"""Normalize environment variable keys and values for consistent comparison."""

from typing import Dict, Optional


def normalize_key(key: str, uppercase: bool = True, strip: bool = True) -> str:
    """Normalize a single environment variable key.

    Args:
        key: The environment variable key.
        uppercase: If True, convert key to uppercase.
        strip: If True, strip surrounding whitespace.

    Returns:
        Normalized key string.
    """
    if strip:
        key = key.strip()
    if uppercase:
        key = key.upper()
    return key


def normalize_value(value: str, strip: bool = True, collapse_whitespace: bool = False) -> str:
    """Normalize a single environment variable value.

    Args:
        value: The environment variable value.
        strip: If True, strip surrounding whitespace.
        collapse_whitespace: If True, collapse internal whitespace runs to a single space.

    Returns:
        Normalized value string.
    """
    if strip:
        value = value.strip()
    if collapse_whitespace:
        import re
        value = re.sub(r'\s+', ' ', value)
    return value


def normalize_env(
    env: Dict[str, str],
    uppercase_keys: bool = True,
    strip_values: bool = True,
    collapse_whitespace: bool = False,
) -> Dict[str, str]:
    """Normalize an entire environment dictionary.

    Args:
        env: Mapping of environment variable keys to values.
        uppercase_keys: If True, convert all keys to uppercase.
        strip_values: If True, strip whitespace from values.
        collapse_whitespace: If True, collapse internal whitespace in values.

    Returns:
        New dict with normalized keys and values.
    """
    result: Dict[str, str] = {}
    for key, value in env.items():
        norm_key = normalize_key(key, uppercase=uppercase_keys)
        norm_val = normalize_value(value, strip=strip_values, collapse_whitespace=collapse_whitespace)
        result[norm_key] = norm_val
    return result


def find_case_conflicts(env: Dict[str, str]) -> Dict[str, list]:
    """Find keys that differ only by case.

    Args:
        env: Mapping of environment variable keys to values.

    Returns:
        Dict mapping uppercase key to list of original keys that collide.
    """
    seen: Dict[str, list] = {}
    for key in env:
        upper = key.upper()
        seen.setdefault(upper, []).append(key)
    return {upper: keys for upper, keys in seen.items() if len(keys) > 1}
