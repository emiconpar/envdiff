"""Tests for envdiff.stringer."""
import pytest
from envdiff.stringer import (
    to_dotenv,
    to_shell_exports,
    to_key_list,
    to_inline,
    to_multiline_comment,
    _quote_if_needed,
)


@pytest.fixture
def sample_env():
    return {"APP_HOST": "localhost", "APP_PORT": "8080", "DB_URL": "postgres://localhost/db"}


def test_to_dotenv_basic(sample_env):
    result = to_dotenv(sample_env)
    assert "APP_HOST=localhost" in result
    assert "APP_PORT=8080" in result


def test_to_dotenv_sorted(sample_env):
    result = to_dotenv(sample_env, sort=True)
    lines = result.splitlines()
    keys = [l.split("=")[0] for l in lines]
    assert keys == sorted(keys)


def test_to_dotenv_with_export(sample_env):
    result = to_dotenv(sample_env, export=True)
    for line in result.splitlines():
        assert line.startswith("export ")


def test_to_shell_exports_uses_export_prefix(sample_env):
    result = to_shell_exports(sample_env)
    assert "export APP_HOST=localhost" in result


def test_to_key_list_sorted(sample_env):
    keys = to_key_list(sample_env, sort=True)
    assert keys == sorted(sample_env.keys())


def test_to_key_list_unsorted(sample_env):
    keys = to_key_list(sample_env, sort=False)
    assert set(keys) == set(sample_env.keys())


def test_to_inline_basic(sample_env):
    result = to_inline(sample_env)
    assert "APP_HOST=localhost" in result
    assert "APP_PORT=8080" in result


def test_to_inline_custom_separator():
    env = {"A": "1", "B": "2"}
    result = to_inline(env, separator=";", sort=True)
    assert result == "A=1;B=2"


def test_to_multiline_comment(sample_env):
    result = to_multiline_comment(sample_env)
    for line in result.splitlines():
        assert line.startswith("# ")


def test_quote_if_needed_empty_value():
    assert _quote_if_needed("") == '""'


def test_quote_if_needed_value_with_space():
    result = _quote_if_needed("hello world")
    assert result == '"hello world"'


def test_quote_if_needed_plain_value():
    assert _quote_if_needed("simple") == "simple"


def test_quote_if_needed_value_with_hash():
    result = _quote_if_needed("val#comment")
    assert result.startswith('"')


def test_to_dotenv_empty_value():
    env = {"EMPTY": ""}
    result = to_dotenv(env)
    assert 'EMPTY=""' in result
