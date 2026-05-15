"""Tests for envdiff.transformer."""

import pytest
from envdiff.transformer import (
    rename_keys,
    remap_values,
    apply_transform,
    prefix_keys,
    strip_key_prefix,
    uppercase_keys,
    lowercase_values,
)


@pytest.fixture
def sample_env():
    return {"APP_HOST": "localhost", "APP_PORT": "8080", "DEBUG": "true"}


# --- rename_keys ---

def test_rename_keys_renames_matching(sample_env):
    result = rename_keys(sample_env, {"APP_HOST": "HOST"})
    assert "HOST" in result
    assert result["HOST"] == "localhost"
    assert "APP_HOST" not in result


def test_rename_keys_keeps_unmatched(sample_env):
    result = rename_keys(sample_env, {"APP_HOST": "HOST"})
    assert "APP_PORT" in result
    assert "DEBUG" in result


def test_rename_keys_target_collision_prefers_renamed(sample_env):
    env = {"OLD": "old_val", "NEW": "existing_val"}
    result = rename_keys(env, {"OLD": "NEW"})
    assert result["NEW"] == "old_val"


def test_rename_keys_empty_mapping(sample_env):
    result = rename_keys(sample_env, {})
    assert result == sample_env


# --- remap_values ---

def test_remap_values_replaces_matching_value(sample_env):
    result = remap_values(sample_env, {"true": "1"})
    assert result["DEBUG"] == "1"


def test_remap_values_leaves_unmatched_values(sample_env):
    result = remap_values(sample_env, {"true": "1"})
    assert result["APP_HOST"] == "localhost"


def test_remap_values_does_not_alter_keys(sample_env):
    result = remap_values(sample_env, {"localhost": "0.0.0.0"})
    assert set(result.keys()) == set(sample_env.keys())


# --- apply_transform ---

def test_apply_transform_modifies_values():
    env = {"KEY": "value"}
    result = apply_transform(env, lambda k, v: (k, v.upper()))
    assert result["KEY"] == "VALUE"


def test_apply_transform_drops_none_entries():
    env = {"KEEP": "yes", "DROP": "no"}
    result = apply_transform(env, lambda k, v: None if k == "DROP" else (k, v))
    assert "DROP" not in result
    assert "KEEP" in result


def test_apply_transform_can_rename_keys():
    env = {"old": "v"}
    result = apply_transform(env, lambda k, v: (k.upper(), v))
    assert "OLD" in result


# --- prefix_keys ---

def test_prefix_keys_adds_prefix(sample_env):
    result = prefix_keys(sample_env, "TEST_")
    for key in result:
        assert key.startswith("TEST_")


def test_prefix_keys_preserves_values(sample_env):
    result = prefix_keys(sample_env, "X_")
    assert result["X_DEBUG"] == "true"


# --- strip_key_prefix ---

def test_strip_key_prefix_removes_prefix(sample_env):
    result = strip_key_prefix(sample_env, "APP_")
    assert "HOST" in result
    assert "PORT" in result
    assert "DEBUG" in result


def test_strip_key_prefix_leaves_non_matching(sample_env):
    result = strip_key_prefix(sample_env, "APP_")
    assert "APP_HOST" not in result
    assert "DEBUG" in result


# --- uppercase_keys / lowercase_values ---

def test_uppercase_keys():
    env = {"host": "localhost", "port": "80"}
    result = uppercase_keys(env)
    assert "HOST" in result
    assert "PORT" in result


def test_lowercase_values():
    env = {"FLAG": "TRUE", "MODE": "Production"}
    result = lowercase_values(env)
    assert result["FLAG"] == "true"
    assert result["MODE"] == "production"
