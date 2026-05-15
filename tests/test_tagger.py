"""Tests for envdiff.tagger and envdiff.tag_report."""

import pytest
from envdiff.tagger import (
    tag_keys,
    keys_for_tag,
    all_tags,
    filter_by_tag,
    untagged_keys,
)
from envdiff.tag_report import format_tag_report, tag_summary


@pytest.fixture
def sample_env():
    return {
        "DB_HOST": "localhost",
        "DB_PASSWORD": "secret",
        "APP_PORT": "8080",
        "LOG_LEVEL": "info",
    }


@pytest.fixture
def tag_map():
    return {
        "database": ["DB_HOST", "DB_PASSWORD"],
        "sensitive": ["DB_PASSWORD"],
        "app": ["APP_PORT"],
    }


def test_tag_keys_assigns_correct_tags(sample_env, tag_map):
    result = tag_keys(sample_env, tag_map)
    assert "database" in result["DB_HOST"]
    assert "database" in result["DB_PASSWORD"]
    assert "sensitive" in result["DB_PASSWORD"]
    assert "app" in result["APP_PORT"]


def test_tag_keys_untagged_key_has_empty_list(sample_env, tag_map):
    result = tag_keys(sample_env, tag_map)
    assert result["LOG_LEVEL"] == []


def test_tag_keys_all_env_keys_present(sample_env, tag_map):
    result = tag_keys(sample_env, tag_map)
    assert set(result.keys()) == set(sample_env.keys())


def test_keys_for_tag_returns_matching_keys(sample_env, tag_map):
    tagged = tag_keys(sample_env, tag_map)
    db_keys = keys_for_tag(tagged, "database")
    assert "DB_HOST" in db_keys
    assert "DB_PASSWORD" in db_keys
    assert "APP_PORT" not in db_keys


def test_keys_for_tag_unknown_tag_returns_empty(sample_env, tag_map):
    tagged = tag_keys(sample_env, tag_map)
    assert keys_for_tag(tagged, "nonexistent") == []


def test_all_tags_returns_sorted_unique(sample_env, tag_map):
    tagged = tag_keys(sample_env, tag_map)
    tags = all_tags(tagged)
    assert tags == sorted(set(tag_map.keys()))


def test_filter_by_tag_returns_subset(sample_env, tag_map):
    tagged = tag_keys(sample_env, tag_map)
    db_env = filter_by_tag(sample_env, tagged, "database")
    assert set(db_env.keys()) == {"DB_HOST", "DB_PASSWORD"}
    assert db_env["DB_HOST"] == "localhost"


def test_filter_by_tag_unknown_tag_returns_empty(sample_env, tag_map):
    tagged = tag_keys(sample_env, tag_map)
    result = filter_by_tag(sample_env, tagged, "ghost")
    assert result == {}


def test_untagged_keys_returns_only_untagged(sample_env, tag_map):
    tagged = tag_keys(sample_env, tag_map)
    untagged = untagged_keys(tagged)
    assert untagged == ["LOG_LEVEL"]


def test_format_tag_report_contains_key(sample_env, tag_map):
    tagged = tag_keys(sample_env, tag_map)
    report = format_tag_report(tagged, label="test", color=False)
    assert "DB_HOST" in report
    assert "database" in report
    assert "test" in report


def test_format_tag_report_shows_untagged(sample_env, tag_map):
    tagged = tag_keys(sample_env, tag_map)
    report = format_tag_report(tagged, color=False)
    assert "(untagged)" in report


def test_tag_summary_contains_counts(sample_env, tag_map):
    tagged = tag_keys(sample_env, tag_map)
    summary = tag_summary(tagged, color=False)
    assert "4 key(s)" in summary
    assert "1 untagged" in summary


def test_format_tag_report_empty_env():
    report = format_tag_report({}, color=False)
    assert "(no keys)" in report
