"""Command-line interface for envdiff."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from envdiff.diff import diff_envs
from envdiff.filter import filter_by_pattern, filter_by_prefix, filter_by_regex
from envdiff.formatter import format_diff, format_summary
from envdiff.parser import parse_env_file
from envdiff.process_env import get_current_env, get_process_env


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="envdiff",
        description="Compare environment variable sets across .env files and processes.",
    )
    p.add_argument("left", help="Left-hand .env file path or 'current' / PID")
    p.add_argument("right", help="Right-hand .env file path or 'current' / PID")
    p.add_argument("--prefix", metavar="PREFIX", action="append", dest="prefixes",
                   help="Filter keys by prefix (repeatable)")
    p.add_argument("--pattern", metavar="GLOB",
                   help="Filter keys by shell glob pattern")
    p.add_argument("--regex", metavar="REGEX",
                   help="Filter keys by regular expression")
    p.add_argument("--exclude", action="store_true",
                   help="Invert the filter (exclude matched keys)")
    p.add_argument("--summary", action="store_true",
                   help="Print summary line only")
    p.add_argument("--no-color", action="store_true",
                   help="Disable ANSI colour output")
    return p


def _load_env(source: str) -> dict:
    """Load an env mapping from a file path, 'current', or a numeric PID."""
    if source == "current":
        return get_current_env()
    if source.isdigit():
        return get_process_env(int(source))
    return parse_env_file(source)


def _apply_filters(env: dict, args: argparse.Namespace) -> dict:
    if args.prefixes:
        env = filter_by_prefix(env, args.prefixes, exclude=args.exclude)
    if args.pattern:
        env = filter_by_pattern(env, args.pattern, exclude=args.exclude)
    if args.regex:
        env = filter_by_regex(env, args.regex, exclude=args.exclude)
    return env


def main(argv: Optional[List[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        left = _apply_filters(_load_env(args.left), args)
        right = _apply_filters(_load_env(args.right), args)
    except (FileNotFoundError, PermissionError, ValueError) as exc:
        print(f"envdiff: error: {exc}", file=sys.stderr)
        return 1

    result = diff_envs(left, right, left_label=args.left, right_label=args.right)
    color = not args.no_color

    if args.summary:
        print(format_summary(result))
    else:
        output = format_diff(result, color=color)
        if output:
            print(output)
        print(format_summary(result))

    return 0 if not result.has_differences() else 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
