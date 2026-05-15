"""Tests for envdiff.parser module."""

import textwrap
from pathlib import Path

import pytest

from envdiff.parser import parse_env_file, parse_env_string


SAMPLE_ENV = textwrap.dedent("""\
    # This is a comment
    APP_NAME=MyApp
    DEBUG=true
    DB_URL="postgresql://localhost/mydb"
    SECRET='s3cr3t'
    export PATH_OVERRIDE=/usr/local/bin
    EMPTY_VAR=
""")


def test_parse_env_string_basic():
    result = parse_env_string(SAMPLE_ENV)
    assert result["APP_NAME"] == "MyApp"
    assert result["DEBUG"] == "true"


def test_parse_env_string_strips_double_quotes():
    result = parse_env_string(SAMPLE_ENV)
    assert result["DB_URL"] == "postgresql://localhost/mydb"


def test_parse_env_string_strips_single_quotes():
    result = parse_env_string(SAMPLE_ENV)
    assert result["SECRET"] == "s3cr3t"


def test_parse_env_string_handles_export_keyword():
    result = parse_env_string(SAMPLE_ENV)
    assert result["PATH_OVERRIDE"] == "/usr/local/bin"


def test_parse_env_string_empty_value():
    result = parse_env_string(SAMPLE_ENV)
    assert result["EMPTY_VAR"] == ""


def test_parse_env_string_ignores_comments():
    result = parse_env_string(SAMPLE_ENV)
    assert not any(k.startswith("#") for k in result)


def test_parse_env_file(tmp_path: Path):
    env_file = tmp_path / ".env"
    env_file.write_text("FOO=bar\nBAZ=qux\n")
    result = parse_env_file(env_file)
    assert result == {"FOO": "bar", "BAZ": "qux"}


def test_parse_env_file_not_found():
    with pytest.raises(FileNotFoundError):
        parse_env_file("/nonexistent/.env")


def test_parse_env_string_no_variables():
    result = parse_env_string("# just a comment\n\n")
    assert result == {}


def test_parse_env_string_inline_comment_not_stripped():
    """Values containing a hash character should be preserved as-is.

    Only full-line comments (lines starting with #) are ignored; inline
    content after a hash is part of the value and must not be removed.
    """
    result = parse_env_string("DESCRIPTION=hello#world\n")
    assert result["DESCRIPTION"] == "hello#world"
