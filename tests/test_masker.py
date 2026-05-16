"""Tests for envdiff.masker."""

import pytest
from envdiff.masker import (
    mask_value,
    partial_mask,
    mask_env,
    masked_keys,
    mask_summary,
    DEFAULT_MASK,
)


@pytest.fixture
def sample_env() -> dict[str, str]:
    return {
        "APP_NAME": "myapp",
        "DB_PASSWORD": "supersecret",
        "API_KEY": "abc123xyz",
        "DEBUG": "true",
    }


def test_mask_value_returns_default_mask():
    assert mask_value("secret") == DEFAULT_MASK


def test_mask_value_custom_mask():
    assert mask_value("secret", mask="[HIDDEN]") == "[HIDDEN]"


def test_partial_mask_reveals_last_chars():
    result = partial_mask("supersecret", reveal_chars=4)
    assert result.endswith("cret")
    assert result.startswith(DEFAULT_MASK)


def test_partial_mask_short_value_fully_masked():
    result = partial_mask("ab", reveal_chars=4)
    assert result == DEFAULT_MASK


def test_partial_mask_empty_value():
    assert partial_mask("") == DEFAULT_MASK


def test_mask_env_masks_specified_keys(sample_env):
    masked = mask_env(sample_env, {"DB_PASSWORD", "API_KEY"})
    assert masked["DB_PASSWORD"] == DEFAULT_MASK
    assert masked["API_KEY"] == DEFAULT_MASK
    assert masked["APP_NAME"] == "myapp"


def test_mask_env_does_not_mutate_original(sample_env):
    original_copy = dict(sample_env)
    mask_env(sample_env, {"DB_PASSWORD"})
    assert sample_env == original_copy


def test_mask_env_partial_mode(sample_env):
    masked = mask_env(sample_env, {"API_KEY"}, partial=True, reveal_chars=3)
    assert masked["API_KEY"].endswith("xyz")
    assert masked["API_KEY"].startswith(DEFAULT_MASK)


def test_mask_env_missing_key_ignored(sample_env):
    masked = mask_env(sample_env, {"NONEXISTENT"})
    assert masked == sample_env


def test_masked_keys_detects_changed_values(sample_env):
    masked = mask_env(sample_env, {"DB_PASSWORD"})
    result = masked_keys(masked, sample_env)
    assert "DB_PASSWORD" in result
    assert "APP_NAME" not in result


def test_mask_summary_correct_counts(sample_env):
    masked = mask_env(sample_env, {"DB_PASSWORD", "API_KEY"})
    summary = mask_summary(masked, sample_env)
    assert summary["masked_count"] == 2
    assert summary["total_keys"] == 4
    assert "DB_PASSWORD" in summary["masked_keys"]
    assert "API_KEY" in summary["masked_keys"]


def test_mask_summary_no_masking(sample_env):
    summary = mask_summary(sample_env, sample_env)
    assert summary["masked_count"] == 0
    assert summary["masked_keys"] == []
