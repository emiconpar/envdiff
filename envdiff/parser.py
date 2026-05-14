"""Parser for .env files into key-value dictionaries."""

import re
from pathlib import Path
from typing import Dict, Optional


_LINE_RE = re.compile(
    r"^\s*(?:export\s+)?"
    r"(?P<key>[A-Za-z_][A-Za-z0-9_]*)"
    r"\s*=\s*"
    r"(?P<value>.*)\s*$"
)
_COMMENT_RE = re.compile(r"^\s*#")


def _strip_quotes(value: str) -> str:
    """Remove surrounding single or double quotes from a value."""
    for quote in ('"', "'"):
        if value.startswith(quote) and value.endswith(quote) and len(value) >= 2:
            return value[1:-1]
    return value


def parse_env_file(path: str | Path) -> Dict[str, str]:
    """Parse a .env file and return a dict of key-value pairs.

    Args:
        path: Path to the .env file.

    Returns:
        Dictionary mapping variable names to their string values.

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    env_path = Path(path)
    if not env_path.exists():
        raise FileNotFoundError(f"env file not found: {env_path}")

    result: Dict[str, str] = {}
    with env_path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line.strip() or _COMMENT_RE.match(line):
                continue
            match = _LINE_RE.match(line)
            if match:
                key = match.group("key")
                value = _strip_quotes(match.group("value").strip())
                result[key] = value
    return result


def parse_env_string(content: str) -> Dict[str, str]:
    """Parse env variable definitions from a raw string.

    Useful for testing or piped input.
    """
    result: Dict[str, str] = {}
    for line in content.splitlines():
        if not line.strip() or _COMMENT_RE.match(line):
            continue
        match = _LINE_RE.match(line)
        if match:
            key = match.group("key")
            value = _strip_quotes(match.group("value").strip())
            result[key] = value
    return result
