"""Tests for envdiff.auditor."""

import pytest
from envdiff.auditor import audit_env, AuditResult, FORBIDDEN_PATTERNS, REQUIRED_KEYS


SAMPLE_CLEAN = {
    "APP_ENV": "development",
    "LOG_LEVEL": "info",
    "PORT": "8080",
}

SAMPLE_DIRTY = {
    "APP_ENV": "development",
    "LOG_LEVEL": "debug",
    "AWS_SECRET_ACCESS_KEY": "abc123",
    "MY_PASSWORD": "hunter2",
}


def test_clean_env_passes():
    result = audit_env(SAMPLE_CLEAN)
    assert result.passed


def test_forbidden_key_detected():
    result = audit_env(SAMPLE_DIRTY)
    assert "AWS_SECRET_ACCESS_KEY" in result.forbidden_found


def test_missing_required_key_detected():
    env = {"LOG_LEVEL": "info"}
    result = audit_env(env)
    assert "APP_ENV" in result.missing_required


def test_plain_secret_detected():
    env = {"APP_ENV": "dev", "LOG_LEVEL": "info", "MY_PASSWORD": "hunter2"}
    result = audit_env(env)
    assert "MY_PASSWORD" in result.plain_secrets


def test_placeholder_value_not_flagged_as_plain_secret():
    env = {"APP_ENV": "dev", "LOG_LEVEL": "info", "API_KEY": "${API_KEY}"}
    result = audit_env(env)
    assert "API_KEY" not in result.plain_secrets


def test_empty_value_in_production_produces_warning():
    env = {"APP_ENV": "production", "LOG_LEVEL": "info", "SOME_VAR": ""}
    result = audit_env(env)
    assert any("SOME_VAR" in w for w in result.warnings)


def test_no_warning_for_empty_value_outside_production():
    env = {"APP_ENV": "development", "LOG_LEVEL": "info", "SOME_VAR": ""}
    result = audit_env(env)
    assert not result.warnings


def test_custom_forbidden_patterns():
    env = {"APP_ENV": "dev", "LOG_LEVEL": "info", "INTERNAL_CERT": "abc"}
    result = audit_env(env, forbidden_patterns=["CERT"])
    assert "INTERNAL_CERT" in result.forbidden_found


def test_custom_required_keys():
    env = {"APP_ENV": "dev"}
    result = audit_env(env, required_keys=["DATABASE_URL"])
    assert "DATABASE_URL" in result.missing_required


def test_label_stored_in_result():
    result = audit_env(SAMPLE_CLEAN, label="my-service")
    assert result.label == "my-service"


def test_passed_false_when_forbidden_present():
    result = audit_env(SAMPLE_DIRTY)
    assert not result.passed
