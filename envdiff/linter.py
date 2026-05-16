"""Lint environment variable sets for common style and convention issues."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

import re

_UPPER_SNAKE = re.compile(r'^[A-Z][A-Z0-9_]*$')
_HAS_LOWER = re.compile(r'[a-z]')
_DOUBLE_UNDERSCORE = re.compile(r'__')
_LEADING_UNDERSCORE = re.compile(r'^_')


@dataclass
class LintResult:
    label: str = "env"
    warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)

    @property
    def clean(self) -> bool:
        return not self.warnings and not self.suggestions

    @property
    def warning_count(self) -> int:
        return len(self.warnings)

    @property
    def suggestion_count(self) -> int:
        return len(self.suggestions)


def lint_env(env: Dict[str, str], label: str = "env") -> LintResult:
    """Lint an environment variable dict and return a LintResult."""
    result = LintResult(label=label)

    for key, value in env.items():
        # Convention: keys should be UPPER_SNAKE_CASE
        if _HAS_LOWER.search(key):
            result.warnings.append(
                f"Key '{key}' contains lowercase letters; prefer UPPER_SNAKE_CASE."
            )

        # Avoid leading underscores (reserved for shell internals)
        if _LEADING_UNDERSCORE.match(key):
            result.warnings.append(
                f"Key '{key}' starts with an underscore; this may conflict with shell internals."
            )

        # Double underscores are unusual and often accidental
        if _DOUBLE_UNDERSCORE.search(key):
            result.suggestions.append(
                f"Key '{key}' contains double underscores; consider simplifying."
            )

        # Warn about values that look like unresolved placeholders
        if value in ("TODO", "FIXME", "CHANGEME", "<REPLACE>", "YOUR_VALUE_HERE"):
            result.warnings.append(
                f"Key '{key}' has a placeholder value '{value}'; replace before use."
            )

        # Suggest trimming if value has leading/trailing whitespace
        if value != value.strip():
            result.suggestions.append(
                f"Key '{key}' value has leading or trailing whitespace."
            )

        # Warn about excessively long values (> 1024 chars)
        if len(value) > 1024:
            result.suggestions.append(
                f"Key '{key}' value is very long ({len(value)} chars); consider externalising."
            )

    return result
