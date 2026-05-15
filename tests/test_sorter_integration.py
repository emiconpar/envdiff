"""Integration tests combining sorter with parser and filter."""

from envdiff.parser import parse_env_string
from envdiff.filter import filter_by_prefix
from envdiff.sorter import sort_env_keys, sort_env_by_prefix, top_n_keys


ENV_TEXT = """
ZEBRA=last
APP_NAME=myapp
DATABASE_URL=postgres://localhost/db
AWS_SECRET=abc123
APP_ENV=production
DB_HOST=localhost
DB_PORT=5432
"""


def test_parse_then_sort_keys_are_ordered():
    env = parse_env_string(ENV_TEXT)
    sorted_env = sort_env_keys(env)
    keys = list(sorted_env.keys())
    assert keys == sorted(keys)


def test_filter_then_sort_prefix_grouping():
    env = parse_env_string(ENV_TEXT)
    db_keys = filter_by_prefix(env, ["DB_", "DATABASE_"])
    sorted_db = sort_env_keys(db_keys)
    keys = list(sorted_db.keys())
    assert keys == sorted(keys)
    assert all(k.startswith(("DB_", "DATABASE_")) for k in keys)


def test_parse_sort_by_prefix_app_first():
    env = parse_env_string(ENV_TEXT)
    result = sort_env_by_prefix(env, prefixes=["APP_", "DB_"])
    keys = list(result.keys())
    app_pos = [i for i, k in enumerate(keys) if k.startswith("APP_")]
    db_pos = [i for i, k in enumerate(keys) if k.startswith("DB_")]
    other_pos = [i for i, k in enumerate(keys) if not k.startswith(("APP_", "DB_"))]
    assert max(app_pos) < min(db_pos)
    assert max(db_pos) < min(other_pos)


def test_top_n_after_parse_returns_correct_count():
    env = parse_env_string(ENV_TEXT)
    result = top_n_keys(env, n=3)
    assert len(result) == 3


def test_full_pipeline_filter_sort_top():
    env = parse_env_string(ENV_TEXT)
    filtered = filter_by_prefix(env, ["APP_", "DB_", "DATABASE_"])
    sorted_env = sort_env_by_prefix(filtered, prefixes=["APP_", "DB_", "DATABASE_"])
    top = top_n_keys(sorted_env, n=2)
    assert len(top) == 2
    # APP_ keys should come first due to prefix ordering
    first_key = list(top.keys())[0]
    assert first_key.startswith("APP_")
