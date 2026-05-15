"""Tests for envdiff.redactor module."""

import pytest
from envdiff.redactor import (
    redact_env,
    redact_keys,
    sensitive_keys,
    DEFAULT_MASK,
)


@pytest.fixture
def sample_env():
    return {
        "DATABASE_PASSWORD": "s3cr3t",
        "API_KEY": "abc123",
        "APP_SECRET": "xyz",
        "AUTH_TOKEN": "tok",
        "HOST": "localhost",
        "PORT": "5432",
        "DEBUG": "true",
    }


def test_redact_env_masks_password(sample_env):
    result = redact_env(sample_env)
    assert result["DATABASE_PASSWORD"] == DEFAULT_MASK


def test_redact_env_masks_api_key(sample_env):
    result = redact_env(sample_env)
    assert result["API_KEY"] == DEFAULT_MASK


def test_redact_env_masks_secret(sample_env):
    result = redact_env(sample_env)
    assert result["APP_SECRET"] == DEFAULT_MASK


def test_redact_env_masks_auth_token(sample_env):
    result = redact_env(sample_env)
    assert result["AUTH_TOKEN"] == DEFAULT_MASK


def test_redact_env_preserves_non_sensitive(sample_env):
    result = redact_env(sample_env)
    assert result["HOST"] == "localhost"
    assert result["PORT"] == "5432"
    assert result["DEBUG"] == "true"


def test_redact_env_does_not_mutate_original(sample_env):
    original_copy = dict(sample_env)
    redact_env(sample_env)
    assert sample_env == original_copy


def test_redact_env_custom_mask(sample_env):
    result = redact_env(sample_env, mask="[HIDDEN]")
    assert result["DATABASE_PASSWORD"] == "[HIDDEN]"


def test_redact_env_custom_patterns():
    env = {"MY_INTERNAL": "value", "OTHER": "data"}
    result = redact_env(env, patterns=[r"(?i)internal"])
    assert result["MY_INTERNAL"] == DEFAULT_MASK
    assert result["OTHER"] == "data"


def test_redact_keys_masks_specified_keys(sample_env):
    result = redact_keys(sample_env, ["HOST", "PORT"])
    assert result["HOST"] == DEFAULT_MASK
    assert result["PORT"] == DEFAULT_MASK
    assert result["DEBUG"] == "true"


def test_redact_keys_empty_list_unchanged(sample_env):
    result = redact_keys(sample_env, [])
    assert result == sample_env


def test_sensitive_keys_returns_matching(sample_env):
    keys = sensitive_keys(sample_env)
    assert "DATABASE_PASSWORD" in keys
    assert "API_KEY" in keys
    assert "APP_SECRET" in keys
    assert "AUTH_TOKEN" in keys


def test_sensitive_keys_excludes_non_sensitive(sample_env):
    keys = sensitive_keys(sample_env)
    assert "HOST" not in keys
    assert "PORT" not in keys


def test_sensitive_keys_custom_patterns():
    env = {"MY_FLAG": "1", "SAFE": "ok"}
    keys = sensitive_keys(env, patterns=[r"(?i)flag"])
    assert keys == ["MY_FLAG"]
