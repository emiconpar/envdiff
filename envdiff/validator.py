"""Validation utilities for environment variable sets."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ValidationResult:
    """Result of validating an environment variable set."""

    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0


_KEY_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$')


def validate_keys(env: Dict[str, str]) -> ValidationResult:
    """Check that all keys are valid POSIX variable names."""
    result = ValidationResult()
    for key in env:
        if not _KEY_RE.match(key):
            result.errors.append(f"Invalid key name: {key!r}")
    return result


def validate_no_empty_values(
    env: Dict[str, str],
    required_keys: Optional[List[str]] = None,
) -> ValidationResult:
    """Warn when values are empty; error if a required key is empty."""
    result = ValidationResult()
    required = set(required_keys or [])
    for key, value in env.items():
        if value == "":
            if key in required:
                result.errors.append(f"Required key has empty value: {key!r}")
            else:
                result.warnings.append(f"Key has empty value: {key!r}")
    return result


def validate_required_keys(
    env: Dict[str, str], required_keys: List[str]
) -> ValidationResult:
    """Error when any required key is missing from *env*."""
    result = ValidationResult()
    for key in required_keys:
        if key not in env:
            result.errors.append(f"Missing required key: {key!r}")
    return result


def validate_env(
    env: Dict[str, str],
    required_keys: Optional[List[str]] = None,
) -> ValidationResult:
    """Run all built-in validations and merge results."""
    combined = ValidationResult()
    checks = [
        validate_keys(env),
        validate_no_empty_values(env, required_keys),
        validate_required_keys(env, required_keys or []),
    ]
    for check in checks:
        combined.errors.extend(check.errors)
        combined.warnings.extend(check.warnings)
    return combined
