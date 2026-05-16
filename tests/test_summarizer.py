"""Tests for envdiff.summarizer."""

import pytest
from envdiff.summarizer import EnvSummary, summarize_env, compare_summaries


@pytest.fixture
def sample_env():
    return {
        "APP_HOST": "localhost",
        "APP_PORT": "8080",
        "DB_HOST": "db.local",
        "DB_PASSWORD": "",
        "SECRET_KEY": "supersecret",
        "X": "y",
    }


def test_summarize_total(sample_env):
    s = summarize_env(sample_env, label="test")
    assert s.total == 6


def test_summarize_label(sample_env):
    s = summarize_env(sample_env, label="production")
    assert s.label == "production"


def test_summarize_empty_count(sample_env):
    s = summarize_env(sample_env)
    assert s.empty_count == 1


def test_summarize_no_empty_values():
    env = {"A": "1", "B": "2"}
    s = summarize_env(env)
    assert s.empty_count == 0


def test_summarize_unique_prefixes(sample_env):
    s = summarize_env(sample_env)
    assert "APP" in s.unique_prefixes
    assert "DB" in s.unique_prefixes
    assert "SECRET" in s.unique_prefixes


def test_summarize_prefix_counts(sample_env):
    s = summarize_env(sample_env)
    assert s.prefix_counts["APP"] == 2
    assert s.prefix_counts["DB"] == 2


def test_summarize_longest_key(sample_env):
    s = summarize_env(sample_env)
    assert s.longest_key == "DB_PASSWORD"


def test_summarize_shortest_key(sample_env):
    s = summarize_env(sample_env)
    assert s.shortest_key == "X"


def test_summarize_longest_value_key(sample_env):
    s = summarize_env(sample_env)
    assert s.longest_value_key == "SECRET_KEY"


def test_summarize_avg_value_length(sample_env):
    s = summarize_env(sample_env)
    total_len = sum(len(v) for v in sample_env.values())
    expected = round(total_len / len(sample_env), 2)
    assert s.avg_value_length == expected


def test_summarize_empty_env():
    s = summarize_env({})
    assert s.total == 0
    assert s.empty_count == 0
    assert s.unique_prefixes == []
    assert s.avg_value_length == 0.0


def test_compare_summaries_total_delta():
    a = summarize_env({"A": "1"}, label="left")
    b = summarize_env({"A": "1", "B": "2"}, label="right")
    cmp = compare_summaries(a, b)
    assert cmp["total_delta"] == 1


def test_compare_summaries_labels():
    a = summarize_env({"A": "1"}, label="left")
    b = summarize_env({"B": "2"}, label="right")
    cmp = compare_summaries(a, b)
    assert cmp["labels"] == ("left", "right")


def test_compare_summaries_empty_delta():
    a = summarize_env({"A": ""}, label="a")
    b = summarize_env({"A": "value"}, label="b")
    cmp = compare_summaries(a, b)
    assert cmp["empty_delta"] == -1
