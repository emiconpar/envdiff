"""Variable interpolation for environment dictionaries.

Supports ${VAR} and $VAR style references within values.
"""

import re
from typing import Dict, Optional

_VAR_PATTERN = re.compile(r'\$\{([^}]+)\}|\$([A-Za-z_][A-Za-z0-9_]*)')


def interpolate_value(value: str, env: Dict[str, str], max_depth: int = 10) -> str:
    """Resolve variable references in a single value string.

    Args:
        value: The string potentially containing $VAR or ${VAR} references.
        env: The environment dictionary to resolve references from.
        max_depth: Maximum recursion depth to prevent infinite loops.

    Returns:
        The value with all resolvable references substituted.
    """
    if max_depth <= 0:
        return value

    def _replace(match: re.Match) -> str:
        var_name = match.group(1) or match.group(2)
        resolved = env.get(var_name, match.group(0))
        if resolved != match.group(0):
            return interpolate_value(resolved, env, max_depth - 1)
        return resolved

    return _VAR_PATTERN.sub(_replace, value)


def interpolate_env(
    env: Dict[str, str],
    context: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """Interpolate all values in an environment dictionary.

    Args:
        env: The environment dictionary whose values should be interpolated.
        context: Optional additional variables to resolve references from.
                 Defaults to env itself if not provided.

    Returns:
        A new dictionary with all values interpolated.
    """
    lookup = {**(context or {}), **env}
    return {key: interpolate_value(value, lookup) for key, value in env.items()}


def find_unresolved(env: Dict[str, str]) -> Dict[str, list]:
    """Find keys whose values contain unresolved variable references.

    Args:
        env: The environment dictionary to inspect.

    Returns:
        A dict mapping key -> list of unresolved variable names.
    """
    unresolved: Dict[str, list] = {}
    for key, value in env.items():
        refs = [m.group(1) or m.group(2) for m in _VAR_PATTERN.finditer(value)]
        missing = [r for r in refs if r not in env]
        if missing:
            unresolved[key] = missing
    return unresolved
