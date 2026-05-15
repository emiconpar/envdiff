"""Tests for envdiff.profiler."""

import pytest
from envdiff.profiler import profile_env, compare_profiles


@pytest.fixture
def sample_env():
    return {
        "APP_HOST": "localhost",
        "APP_PORT": "8080",
        "APP_SECRET": "",
        "DB_HOST": "db.local",
        "DB_PORT": "5432",
        "STANDALONE": "yes",
    }


def test_profile_total_keys(sample_env):
    result = profile_env(sample_env, label="test")
    assert result.total_keys == 6


def test_profile_label(sample_env):
    result = profile_env(sample_env, label="myenv")
    assert result.label == "myenv"


def test_profile_empty_values(sample_env):
    result = profile_env(sample_env)
    assert "APP_SECRET" in result.empty_values
    assert len(result.empty_values) == 1


def test_profile_no_empty_values():
    env = {"KEY": "value", "OTHER": "data"}
    result = profile_env(env)
    assert result.empty_values == []


def test_profile_prefix_counts(sample_env):
    result = profile_env(sample_env)
    assert result.prefixes.get("APP") == 3
    assert result.prefixes.get("DB") == 2


def test_profile_top_prefixes_limited(sample_env):
    result = profile_env(sample_env, top_n=1)
    assert len(result.top_prefixes) == 1
    assert result.top_prefixes[0][0] == "APP"


def test_profile_longest_key(sample_env):
    result = profile_env(sample_env)
    assert result.longest_key == "STANDALONE"


def test_profile_longest_value_key(sample_env):
    result = profile_env(sample_env)
    assert result.longest_value_key == "DB_HOST"


def test_profile_empty_env():
    result = profile_env({}, label="empty")
    assert result.total_keys == 0
    assert result.empty_values == []
    assert result.prefixes == {}


def test_compare_profiles_keys(sample_env):
    left = profile_env(sample_env, label="left")
    right = profile_env({"X": "1", "Y": "2"}, label="right")
    cmp = compare_profiles(left, right)
    assert cmp["total_keys"]["left"] == 6
    assert cmp["total_keys"]["right"] == 2


def test_compare_profiles_empty_values(sample_env):
    left = profile_env(sample_env, label="left")
    right = profile_env({"A": "", "B": ""}, label="right")
    cmp = compare_profiles(left, right)
    assert cmp["empty_values"]["left"] == 1
    assert cmp["empty_values"]["right"] == 2
