"""Tests for envdiff.filter module."""

import pytest

from envdiff.filter import (
    filter_by_pattern,
    filter_by_prefix,
    filter_by_regex,
    select_keys,
)

SAMPLE: dict = {
    "AWS_ACCESS_KEY_ID": "AKIA123",
    "AWS_SECRET_ACCESS_KEY": "secret",
    "DATABASE_URL": "postgres://localhost/db",
    "DEBUG": "true",
    "PORT": "8080",
}


def test_filter_by_prefix_keep():
    result = filter_by_prefix(SAMPLE, ["AWS_"])
    assert set(result.keys()) == {"AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"}


def test_filter_by_prefix_exclude():
    result = filter_by_prefix(SAMPLE, ["AWS_"], exclude=True)
    assert "AWS_ACCESS_KEY_ID" not in result
    assert "DATABASE_URL" in result


def test_filter_by_prefix_multiple_prefixes():
    result = filter_by_prefix(SAMPLE, ["AWS_", "DATABASE_"])
    assert "AWS_ACCESS_KEY_ID" in result
    assert "DATABASE_URL" in result
    assert "DEBUG" not in result


def test_filter_by_prefix_no_match_returns_empty():
    result = filter_by_prefix(SAMPLE, ["NONEXISTENT_"])
    assert result == {}


def test_filter_by_pattern_wildcard():
    result = filter_by_pattern(SAMPLE, "AWS_*")
    assert set(result.keys()) == {"AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"}


def test_filter_by_pattern_exclude():
    result = filter_by_pattern(SAMPLE, "AWS_*", exclude=True)
    assert "AWS_ACCESS_KEY_ID" not in result
    assert len(result) == 3


def test_filter_by_pattern_exact_match():
    result = filter_by_pattern(SAMPLE, "PORT")
    assert result == {"PORT": "8080"}


def test_filter_by_pattern_no_match():
    result = filter_by_pattern(SAMPLE, "REDIS_*")
    assert result == {}


def test_filter_by_regex_keep():
    result = filter_by_regex(SAMPLE, r"^AWS_")
    assert set(result.keys()) == {"AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"}


def test_filter_by_regex_exclude():
    result = filter_by_regex(SAMPLE, r"_URL$", exclude=True)
    assert "DATABASE_URL" not in result
    assert "DEBUG" in result


def test_filter_by_regex_invalid_raises():
    import re
    with pytest.raises(re.error):
        filter_by_regex(SAMPLE, r"[invalid")


def test_select_keys_present():
    result = select_keys(SAMPLE, ["DEBUG", "PORT"])
    assert result == {"DEBUG": "true", "PORT": "8080"}


def test_select_keys_missing_ignored():
    result = select_keys(SAMPLE, ["DEBUG", "MISSING_KEY"])
    assert result == {"DEBUG": "true"}


def test_select_keys_empty_list():
    result = select_keys(SAMPLE, [])
    assert result == {}
