"""Convert env dicts to various string representations."""
from __future__ import annotations

from typing import Dict, List, Optional


def to_dotenv(env: Dict[str, str], sort: bool = False, export: bool = False) -> str:
    """Render an env dict as a .env file string."""
    items = sorted(env.items()) if sort else env.items()
    prefix = "export " if export else ""
    lines = [f"{prefix}{k}={_quote_if_needed(v)}" for k, v in items]
    return "\n".join(lines)


def to_shell_exports(env: Dict[str, str], sort: bool = False) -> str:
    """Render an env dict as shell export statements."""
    return to_dotenv(env, sort=sort, export=True)


def to_key_list(env: Dict[str, str], sort: bool = True) -> List[str]:
    """Return a sorted (or original-order) list of keys."""
    keys = list(env.keys())
    return sorted(keys) if sort else keys


def to_inline(env: Dict[str, str], separator: str = " ", sort: bool = False) -> str:
    """Render env as a single inline string suitable for a command prefix."""
    items = sorted(env.items()) if sort else env.items()
    return separator.join(f"{k}={_quote_if_needed(v)}" for k, v in items)


def to_multiline_comment(env: Dict[str, str], sort: bool = False) -> str:
    """Render env as commented-out lines (useful for documentation)."""
    items = sorted(env.items()) if sort else env.items()
    lines = [f"# {k}={_quote_if_needed(v)}" for k, v in items]
    return "\n".join(lines)


def _quote_if_needed(value: str) -> str:
    """Wrap value in double quotes if it contains spaces or special characters."""
    if not value:
        return "\"\""
    needs_quoting = any(c in value for c in (" ", "\t", "#", "$", "'", '"', ";", "&", "|", ">", "<"))
    if needs_quoting:
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    return value
