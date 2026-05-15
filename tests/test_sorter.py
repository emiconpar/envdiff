"""Tests for envdiff.sorter."""

import pytest
from envdiff.sorter import (
    sort_env_keys,
    sort_env_by_value,
    sort_env_by_prefix,
    top_n_keys,
)


@pytest.fixture
def sample_env():
    return {
        "ZEBRA": "last",
        "APP_NAME": "myapp",
        "DATABASE_URL": "postgres://localhost/db",
        "AWS_SECRET": "abc123",
        "APP_ENV": "production",
    }


def test_sort_env_keys_alphabetical(sample_env):
    result = sort_env_keys(sample_env)
    assert list(result.keys()) == sorted(sample_env.keys())


def test_sort_env_keys_reverse(sample_env):
    result = sort_env_keys(sample_env, reverse=True)
    assert list(result.keys()) == sorted(sample_env.keys(), reverse=True)


def test_sort_env_keys_preserves_values(sample_env):
    result = sort_env_keys(sample_env)
    for k, v in sample_env.items():
        assert result[k] == v


def test_sort_env_by_value(sample_env):
    result = sort_env_by_value(sample_env)
    values = list(result.values())
    assert values == sorted(sample_env.values())


def test_sort_env_by_value_reverse(sample_env):
    result = sort_env_by_value(sample_env, reverse=True)
    values = list(result.values())
    assert values == sorted(sample_env.values(), reverse=True)


def test_sort_env_by_prefix_groups_correctly(sample_env):
    result = sort_env_by_prefix(sample_env, prefixes=["APP_", "AWS_"])
    keys = list(result.keys())
    app_indices = [i for i, k in enumerate(keys) if k.startswith("APP_")]
    aws_indices = [i for i, k in enumerate(keys) if k.startswith("AWS_")]
    other_indices = [i for i, k in enumerate(keys) if not k.startswith(("APP_", "AWS_"))]
    assert max(app_indices) < min(aws_indices)
    assert max(aws_indices) < min(other_indices)


def test_sort_env_by_prefix_no_match_falls_to_end():
    env = {"ZEBRA": "z", "ALPHA": "a"}
    result = sort_env_by_prefix(env, prefixes=["DB_"])
    # No matches – all go to remainder, sorted alphabetically
    assert list(result.keys()) == ["ALPHA", "ZEBRA"]


def test_top_n_keys_by_key(sample_env):
    result = top_n_keys(sample_env, n=2, by="key")
    assert len(result) == 2
    assert list(result.keys()) == sorted(sample_env.keys())[:2]


def test_top_n_keys_by_value(sample_env):
    result = top_n_keys(sample_env, n=3, by="value")
    assert len(result) == 3
    assert list(result.values()) == sorted(sample_env.values())[:3]


def test_top_n_keys_invalid_by_raises():
    with pytest.raises(ValueError, match="Unknown sort criterion"):
        top_n_keys({"A": "1"}, n=1, by="length")


def test_top_n_larger_than_dict_returns_all(sample_env):
    result = top_n_keys(sample_env, n=100)
    assert len(result) == len(sample_env)
