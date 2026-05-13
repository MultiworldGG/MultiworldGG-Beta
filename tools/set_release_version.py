#!/usr/bin/env python3
"""Set release version strings used by packaging files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


APPLICATION_VERSION_RE = re.compile(
    r'^(?P<prefix>\s*app_version:\s*)["\']?(?P<version>[^"\'\s#]+)["\']?(?P<suffix>\s*(?:#.*)?)$',
    re.MULTILINE,
)
INNO_VERSION_RE = re.compile(
    r'(?P<prefix>#define\s+MyAppVersionText\s+ReadIni\(SourcePath \+ "\\setup\.ini", "Data", "app_version", ")'
    r'(?P<version>[^"]+)'
    r'(?P<suffix>"\))'
)


def normalize_version(version: str) -> str:
    """Accept refs/tags/<tag> or raw tags from GitHub Actions."""
    version = version.strip()
    if version.startswith("refs/tags/"):
        version = version.removeprefix("refs/tags/")
    if not version:
        raise ValueError("version cannot be empty")
    return version


def replace_version(path: Path, pattern: re.Pattern[str], version: str, *, quote: bool = False) -> bool:
    text = path.read_text(encoding="utf-8")

    match = pattern.search(text)
    if not match:
        raise ValueError(f"could not find version string in {path}")

    current_version = match.group("version")
    if current_version == version:
        print(f"{path}: already {version}")
        return False

    replacement_version = f'"{version}"' if quote else version
    updated = pattern.sub(
        lambda current_match: (
            f'{current_match.group("prefix")}{replacement_version}{current_match.group("suffix")}'
        ),
        text,
        count=1,
    )
    path.write_text(updated, encoding="utf-8")
    print(f"{path}: {current_version} -> {version}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Update application.yaml and inno_setup.iss to a release tag version."
    )
    parser.add_argument("version", help="Release version or tag, for example 0.8.0b8")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root containing application.yaml and inno_setup.iss",
    )
    args = parser.parse_args()

    try:
        version = normalize_version(args.version)
        root = args.root.resolve()
        replace_version(root / "application.yaml", APPLICATION_VERSION_RE, version, quote=True)
        replace_version(root / "inno_setup.iss", INNO_VERSION_RE, version)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
