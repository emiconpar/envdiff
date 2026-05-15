"""Tests for envdiff.validator."""

import pytest
from envdiff.validator import (
    ValidationResult,
    validate_keys,
    validate_no_empty_values,
    validate_required_keys,
    validate_env,
)


# ---------------------------------------------------------------------------
# validate_keys
# ---------------------------------------------------------------------------

def test_valid_keys_pass():
    result = validate_keys({"FOO": "bar", "_UNDER": "1", "MixedCase123": "x"})
    assert result.is_valid
    assert not result.has_warnings


def test_key_starting_with_digit_is_invalid():
    result = validate_keys({"1BAD": "value"})
    assert not result.is_valid
    assert any("1BAD" in e for e in result.errors)


def test_key_with_hyphen_is_invalid():
    result = validate_keys({"BAD-KEY": "value"})
    assert not result.is_valid


def test_multiple_invalid_keys_all_reported():
    result = validate_keys({"1A": "", "2B": "", "OK": ""})
    assert len(result.errors) == 2


# ---------------------------------------------------------------------------
# validate_no_empty_values
# ---------------------------------------------------------------------------

def test_empty_value_produces_warning():
    result = validate_no_empty_values({"FOO": ""})
    assert result.is_valid
    assert result.has_warnings
    assert any("FOO" in w for w in result.warnings)


def test_non_empty_values_no_warnings():
    result = validate_no_empty_values({"FOO": "bar"})
    assert result.is_valid
    assert not result.has_warnings


def test_required_key_with_empty_value_is_error():
    result = validate_no_empty_values({"SECRET": ""}, required_keys=["SECRET"])
    assert not result.is_valid
    assert any("SECRET" in e for e in result.errors)


# ---------------------------------------------------------------------------
# validate_required_keys
# ---------------------------------------------------------------------------

def test_present_required_keys_pass():
    result = validate_required_keys({"A": "1", "B": "2"}, ["A", "B"])
    assert result.is_valid


def test_missing_required_key_is_error():
    result = validate_required_keys({"A": "1"}, ["A", "MISSING"])
    assert not result.is_valid
    assert any("MISSING" in e for e in result.errors)


# ---------------------------------------------------------------------------
# validate_env (combined)
# ---------------------------------------------------------------------------

def test_validate_env_clean():
    result = validate_env({"HOST": "localhost", "PORT": "5432"}, required_keys=["HOST", "PORT"])
    assert result.is_valid


def test_validate_env_aggregates_all_issues():
    env = {"1BAD": "x", "MISSING_VAL": ""}
    result = validate_env(env, required_keys=["MUST_EXIST"])
    # invalid key + missing required key
    assert len(result.errors) >= 2


def test_validate_env_no_required_keys_arg():
    result = validate_env({"GOOD": "val"})
    assert result.is_valid
