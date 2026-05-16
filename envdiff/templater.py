"""Template rendering for .env files using a base env as context."""

from __future__ import annotations

import re
from typing import Dict, List, Optional

_TEMPLATE_RE = re.compile(r"\{\{\s*(\w+)\s*\}\}")


def render_template(template: str, context: Dict[str, str]) -> str:
    """Replace {{ KEY }} placeholders in *template* with values from *context*.

    Unknown placeholders are left untouched.
    """

    def _replace(match: re.Match) -> str:  # type: ignore[type-arg]
        key = match.group(1)
        return context.get(key, match.group(0))

    return _TEMPLATE_RE.sub(_replace, template)


def render_env_template(
    template_env: Dict[str, str],
    context: Dict[str, str],
) -> Dict[str, str]:
    """Render every value in *template_env* using *context* as the substitution
    source.  Keys are never modified."""
    return {key: render_template(value, context) for key, value in template_env.items()}


def find_unrendered(env: Dict[str, str]) -> List[str]:
    """Return keys whose values still contain ``{{ ... }}`` placeholders."""
    return [
        key
        for key, value in env.items()
        if _TEMPLATE_RE.search(value)
    ]


def template_summary(
    original: Dict[str, str],
    rendered: Dict[str, str],
    label: Optional[str] = None,
) -> Dict[str, object]:
    """Return a summary dict describing what changed during rendering."""
    changed = [
        key
        for key in original
        if original[key] != rendered.get(key, original[key])
    ]
    unrendered = find_unrendered(rendered)
    return {
        "label": label or "env",
        "total": len(original),
        "rendered_count": len(changed),
        "unrendered_count": len(unrendered),
        "rendered_keys": changed,
        "unrendered_keys": unrendered,
    }
