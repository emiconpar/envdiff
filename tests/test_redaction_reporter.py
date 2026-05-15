"""Tests for envdiff.redaction_reporter."""

import pytest
from envdiff.redaction_reporter import (
    redact_and_diff,
    format_redacted_diff,
    redacted_summary,
    list_redacted_keys,
)


LEFT = {
    "APP_NAME": "myapp",
    "DB_PASSWORD": "secret123",
    "API_KEY": "key-abc",
    "PORT": "8080",
}

RIGHT = {
    "APP_NAME": "myapp",
    "DB_PASSWORD": "newsecret",
    "API_KEY": "key-abc",
    "PORT": "9090",
    "NEW_VAR": "hello",
}


def test_redact_and_diff_returns_result():
    result = redact_and_diff(LEFT, RIGHT)
    assert result is not None


def test_redact_and_diff_sensitive_values_are_masked():
    result = redact_and_diff(LEFT, RIGHT)
    # DB_PASSWORD changed but both sides should be redacted so it appears unchanged
    assert "DB_PASSWORD" not in result.changed


def test_redact_and_diff_api_key_masked_appears_unchanged():
    result = redact_and_diff(LEFT, RIGHT)
    assert "API_KEY" not in result.changed


def test_redact_and_diff_non_sensitive_change_detected():
    result = redact_and_diff(LEFT, RIGHT)
    assert "PORT" in result.changed


def test_redact_and_diff_only_in_right():
    result = redact_and_diff(LEFT, RIGHT)
    assert "NEW_VAR" in result.only_in_right


def test_format_redacted_diff_is_string():
    output = format_redacted_diff(LEFT, RIGHT)
    assert isinstance(output, str)


def test_format_redacted_diff_contains_port():
    output = format_redacted_diff(LEFT, RIGHT, color=False)
    assert "PORT" in output


def test_format_redacted_diff_contains_labels():
    output = format_redacted_diff(LEFT, RIGHT, left_label="prod", right_label="dev", color=False)
    assert "prod" in output
    assert "dev" in output


def test_format_redacted_diff_no_plain_secret_values():
    output = format_redacted_diff(LEFT, RIGHT, color=False)
    assert "secret123" not in output
    assert "newsecret" not in output


def test_redacted_summary_is_string():
    summary = redacted_summary(LEFT, RIGHT)
    assert isinstance(summary, str)


def test_redacted_summary_mentions_added():
    summary = redacted_summary(LEFT, RIGHT)
    assert "added" in summary


def test_list_redacted_keys_finds_password():
    keys = list_redacted_keys(LEFT)
    assert "DB_PASSWORD" in keys


def test_list_redacted_keys_finds_api_key():
    keys = list_redacted_keys(LEFT)
    assert "API_KEY" in keys


def test_list_redacted_keys_excludes_non_sensitive():
    keys = list_redacted_keys(LEFT)
    assert "APP_NAME" not in keys
    assert "PORT" not in keys


def test_list_redacted_keys_extra_sensitive():
    keys = list_redacted_keys(LEFT, extra_sensitive=["PORT"])
    assert "PORT" in keys


def test_list_redacted_keys_returns_sorted():
    keys = list_redacted_keys(LEFT)
    assert keys == sorted(keys)
