"""Tests for envdiff.linter module."""

import pytest
from envdiff.linter import lint_env, LintResult


@pytest.fixture
def clean_env():
    return {
        "DATABASE_URL": "postgres://localhost/db",
        "APP_PORT": "8080",
        "LOG_LEVEL": "INFO",
    }


def test_clean_env_has_no_issues(clean_env):
    result = lint_env(clean_env)
    assert result.clean
    assert result.warning_count == 0
    assert result.suggestion_count == 0


def test_label_is_set():
    result = lint_env({}, label="production")
    assert result.label == "production"


def test_lowercase_key_produces_warning():
    result = lint_env({"db_host": "localhost"})
    assert result.warning_count == 1
    assert any("db_host" in w for w in result.warnings)


def test_mixed_case_key_produces_warning():
    result = lint_env({"DbHost": "localhost"})
    assert result.warning_count >= 1
    assert any("DbHost" in w for w in result.warnings)


def test_leading_underscore_key_produces_warning():
    result = lint_env({"_INTERNAL": "value"})
    assert any("_INTERNAL" in w for w in result.warnings)


def test_double_underscore_produces_suggestion():
    result = lint_env({"APP__PORT": "8080"})
    assert any("APP__PORT" in s for s in result.suggestions)


def test_placeholder_value_produces_warning():
    for placeholder in ("TODO", "FIXME", "CHANGEME", "<REPLACE>", "YOUR_VALUE_HERE"):
        result = lint_env({"SOME_KEY": placeholder})
        assert result.warning_count >= 1, f"Expected warning for placeholder '{placeholder}'"


def test_whitespace_value_produces_suggestion():
    result = lint_env({"API_KEY": "  abc  "})
    assert any("API_KEY" in s for s in result.suggestions)


def test_very_long_value_produces_suggestion():
    result = lint_env({"BIG_BLOB": "x" * 1025})
    assert any("BIG_BLOB" in s for s in result.suggestions)


def test_exactly_1024_chars_no_suggestion():
    result = lint_env({"BIG_BLOB": "x" * 1024})
    assert not any("BIG_BLOB" in s for s in result.suggestions)


def test_multiple_issues_accumulated():
    env = {
        "bad_key": "TODO",
        "GOOD_KEY": "ok",
        "another_bad": "  spaced  ",
    }
    result = lint_env(env)
    assert result.warning_count >= 2  # lowercase + placeholder
    assert result.suggestion_count >= 1  # whitespace


def test_clean_result_property():
    result = LintResult(label="test")
    assert result.clean
    result.warnings.append("something")
    assert not result.clean


def test_empty_env_is_clean():
    result = lint_env({})
    assert result.clean
