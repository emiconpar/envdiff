"""Tests for envdiff.normalizer module."""

import pytest
from envdiff.normalizer import (
    normalize_key,
    normalize_value,
    normalize_env,
    find_case_conflicts,
)


def test_normalize_key_uppercase():
    assert normalize_key("my_key") == "MY_KEY"


def test_normalize_key_strips_whitespace():
    assert normalize_key("  KEY  ") == "KEY"


def test_normalize_key_no_uppercase():
    assert normalize_key("my_key", uppercase=False) == "my_key"


def test_normalize_key_no_strip():
    assert normalize_key("  key  ", strip=False) == "  KEY  "


def test_normalize_value_strips_whitespace():
    assert normalize_value("  hello  ") == "hello"


def test_normalize_value_no_strip():
    assert normalize_value("  hello  ", strip=False) == "  hello  "


def test_normalize_value_collapse_whitespace():
    assert normalize_value("hello   world", collapse_whitespace=True) == "hello world"


def test_normalize_value_collapse_and_strip():
    assert normalize_value("  hello   world  ", strip=True, collapse_whitespace=True) == "hello world"


def test_normalize_value_no_change_needed():
    assert normalize_value("simple") == "simple"


def test_normalize_env_keys_uppercased():
    env = {"key": "value", "another": "val"}
    result = normalize_env(env)
    assert "KEY" in result
    assert "ANOTHER" in result


def test_normalize_env_values_stripped():
    env = {"KEY": "  value  "}
    result = normalize_env(env)
    assert result["KEY"] == "value"


def test_normalize_env_preserves_all_keys():
    env = {"a": "1", "b": "2", "c": "3"}
    result = normalize_env(env)
    assert len(result) == 3


def test_normalize_env_collapse_whitespace():
    env = {"KEY": "foo   bar"}
    result = normalize_env(env, collapse_whitespace=True)
    assert result["KEY"] == "foo bar"


def test_normalize_env_no_uppercase():
    env = {"myKey": "value"}
    result = normalize_env(env, uppercase_keys=False)
    assert "myKey" in result
    assert "MYKEY" not in result


def test_find_case_conflicts_detects_collision():
    env = {"key": "a", "KEY": "b", "Key": "c"}
    conflicts = find_case_conflicts(env)
    assert "KEY" in conflicts
    assert len(conflicts["KEY"]) == 3


def test_find_case_conflicts_no_conflicts():
    env = {"ALPHA": "1", "BETA": "2"}
    conflicts = find_case_conflicts(env)
    assert conflicts == {}


def test_find_case_conflicts_partial():
    env = {"foo": "1", "FOO": "2", "BAR": "3"}
    conflicts = find_case_conflicts(env)
    assert "FOO" in conflicts
    assert "BAR" not in conflicts
