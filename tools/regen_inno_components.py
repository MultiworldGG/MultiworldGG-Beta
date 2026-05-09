#!/usr/bin/env python3
"""
Regenerate the autogen regions of src/inno_setup.iss from the published
mwgg_igdb game-index variant package.

Three regions are managed:
  - in_client       : `#define InClientDescriptions "..."` near the top
  - components      : the entire `[Components]` block
  - dispatch        : the body of `GetSelectedWorld` that maps slugs to
                      `worlds.<slug>` tokens

Each region is delimited by `BEGIN AUTOGEN: <name>` / `END AUTOGEN: <name>`
markers; everything outside the markers is left untouched.

Disk-size policy:
  - Prefer `disk_space_kb` from the manifest (author-stamped via per-world CI).
  - Fall back to the value parsed out of the existing iss file for worlds that
    haven't yet rolled out the gen-pymod-release size step.
  - If both are missing, emit a warning and use 0.

The script is idempotent: same input -> byte-identical output.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

DEFAULT_ISS = Path(__file__).resolve().parent.parent / "inno_setup.iss"
DEFAULT_VARIANT = "sixteen"
INDEX_REPO = "MultiworldGG/MultiworldGG-Index"


# ----------------------------- iss file parsing -----------------------------

REGION_PATTERN = re.compile(
    r"(?P<begin>^[ \t]*(?:;|//) BEGIN AUTOGEN: (?P<name>[a-z_]+).*?\n)"
    r"(?P<body>.*?)"
    r"(?P<end>^[ \t]*(?:;|//) END AUTOGEN: (?P=name).*?\n)",
    re.DOTALL | re.MULTILINE,
)

# Matches: Name: "<slug>"; Description: "<game>"; ExtraDiskSpaceRequired: <kb>
COMPONENT_LINE = re.compile(
    r'^\s*Name:\s*"(?P<slug>[^"]+)";\s*Description:\s*"(?P<desc>[^"]+)";'
    r'\s*ExtraDiskSpaceRequired:\s*(?P<size>[\d_]+)\s*$',
    re.MULTILINE,
)


def parse_existing_components(iss_text: str) -> dict[str, dict[str, Any]]:
    """Parse the current `[Components]` autogen body to build a fallback table.

    Returns: { slug: { "description": ..., "disk_space_kb": int } }
    """
    out: dict[str, dict[str, Any]] = {}
    region = _find_region(iss_text, "components")
    if region is None:
        return out
    for m in COMPONENT_LINE.finditer(region):
        out[m["slug"]] = {
            "description": m["desc"],
            "disk_space_kb": int(m["size"].replace("_", "")),
        }
    return out


def _find_region(iss_text: str, name: str) -> str | None:
    for m in REGION_PATTERN.finditer(iss_text):
        if m["name"] == name:
            return m["body"]
    return None


def replace_region(iss_text: str, name: str, new_body: str) -> str:
    """Replace the body of a single AUTOGEN region in iss_text.

    Raises if the named region isn't present.
    """
    if not new_body.endswith("\n"):
        new_body += "\n"

    def _sub(m: re.Match[str]) -> str:
        if m["name"] != name:
            return m.group(0)
        return f"{m['begin']}{new_body}{m['end']}"

    new_text, count = REGION_PATTERN.subn(_sub, iss_text)
    if not any(m["name"] == name for m in REGION_PATTERN.finditer(iss_text)):
        raise RuntimeError(f"AUTOGEN region '{name}' not found in iss file")
    return new_text


# --------------------------- mwgg_igdb loading ------------------------------


def _try_install_mwgg_igdb(variant: str) -> None:
    branch = f"game_index_{variant}"
    url = f"git+https://github.com/{INDEX_REPO}@{branch}"
    print(f"[regen] installing mwgg_igdb from {branch}", file=sys.stderr)
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", "--no-cache-dir", url],
        check=True,
    )


def load_index(variant: str) -> dict[str, dict[str, Any]]:
    """Return the GameIndex's `get_all_games()` dict, installing if missing."""
    try:
        from mwgg_igdb import GameIndex  # type: ignore
    except ImportError:
        _try_install_mwgg_igdb(variant)
        from importlib import invalidate_caches
        invalidate_caches()
        from mwgg_igdb import GameIndex  # type: ignore
    return dict(GameIndex.get_all_games())


# ---------------------------- region rendering ------------------------------


def _format_kb(value: int) -> str:
    """Render an int as Inno Setup's underscore-separated thousands grouping."""
    s = str(value)
    out = []
    while len(s) > 3:
        out.append(s[-3:])
        s = s[:-3]
    out.append(s)
    return "_".join(reversed(out))


def render_components(
    games: dict[str, dict[str, Any]],
    fallback: dict[str, dict[str, Any]],
) -> str:
    lines: list[str] = []
    for slug in sorted(games.keys()):
        manifest = games[slug]
        description = manifest.get("game") or fallback.get(slug, {}).get("description") or slug
        size = manifest.get("disk_space_kb")
        if size is None:
            fb = fallback.get(slug, {})
            if "disk_space_kb" in fb:
                size = fb["disk_space_kb"]
            else:
                print(
                    f"[regen] warning: no disk_space_kb for '{slug}' (manifest "
                    f"missing field, no fallback in current iss); using 0",
                    file=sys.stderr,
                )
                size = 0
        size_text = _format_kb(int(size))
        # Escape any embedded quotes in the description, defensively.
        desc = description.replace('"', '""')
        lines.append(
            f'Name: "{slug}"; Description: "{desc}"; ExtraDiskSpaceRequired: {size_text}'
        )
    return "\n".join(lines) + "\n"


def render_dispatch(games: dict[str, dict[str, Any]]) -> str:
    lines: list[str] = []
    for slug in sorted(games.keys()):
        lines.append(
            f"  if WizardIsComponentSelected('worlds\\{slug}') then "
            f"WorldList := WorldList + ' worlds.{slug}';"
        )
    return "\n".join(lines) + "\n"


def render_in_client_descriptions(games: dict[str, dict[str, Any]]) -> str:
    in_client_descs = sorted(
        manifest.get("game") or slug
        for slug, manifest in games.items()
        if "in_client" in (manifest.get("flags") or [])
    )
    # TStringList.CommaText treats both whitespace and commas as separators
    # unless an item is double-quoted. Quote every item so descriptions like
    # "A Hat in Time" round-trip as a single entry. Embedded double-quotes are
    # escaped by doubling per Delphi convention. The whole iss-side string is
    # single-quoted in the Pascal code, so double-quotes don't need escaping
    # at the iss preprocessor level.
    quoted = [f'""{d.replace(chr(34), chr(34) * 2)}""' for d in in_client_descs]
    joined = ",".join(quoted)
    return f'#define InClientDescriptions "{joined}"\n'


# -------------------------------- diff log ----------------------------------


def diff_summary(
    old_components: dict[str, dict[str, Any]],
    games: dict[str, dict[str, Any]],
) -> str:
    old_set = set(old_components.keys())
    new_set = set(games.keys())
    added = sorted(new_set - old_set)
    removed = sorted(old_set - new_set)
    changed: list[str] = []
    for slug in sorted(old_set & new_set):
        old = old_components[slug]
        new = games[slug]
        new_desc = new.get("game") or slug
        new_size = new.get("disk_space_kb")
        if new_size is None:
            new_size = old["disk_space_kb"]
        if old["description"] != new_desc or old["disk_space_kb"] != int(new_size):
            changed.append(slug)
    parts = []
    if added:
        parts.append(f"added: {', '.join(added)}")
    if removed:
        parts.append(f"removed: {', '.join(removed)}")
    if changed:
        parts.append(f"changed: {', '.join(changed)}")
    return "; ".join(parts) if parts else "no changes"


# --------------------------------- main -------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--iss", type=Path, default=DEFAULT_ISS,
        help="Path to inno_setup.iss (default: src/inno_setup.iss)",
    )
    p.add_argument(
        "--variant", default=DEFAULT_VARIANT,
        choices=("sixteen", "twelve", "ao", "nr"),
        help="mwgg_igdb variant to read from (default: sixteen)",
    )
    p.add_argument(
        "--from-json", type=Path, default=None,
        help="Read the games dict from a JSON file instead of mwgg_igdb. "
             "Schema: { '<slug>': { 'game': str, 'flags': [..], 'disk_space_kb': int } }",
    )
    p.add_argument(
        "--check", action="store_true",
        help="Exit with code 1 if regeneration would change the file. Don't write.",
    )
    args = p.parse_args(argv)

    iss_path: Path = args.iss
    iss_text = iss_path.read_text(encoding="utf-8")

    if args.from_json is not None:
        games = json.loads(args.from_json.read_text(encoding="utf-8"))
    else:
        games = load_index(args.variant)

    fallback = parse_existing_components(iss_text)

    new_iss = iss_text
    new_iss = replace_region(new_iss, "components", render_components(games, fallback))
    new_iss = replace_region(new_iss, "dispatch", render_dispatch(games))
    new_iss = replace_region(new_iss, "in_client", render_in_client_descriptions(games))

    summary = diff_summary(fallback, games)
    print(f"[regen] {summary}", file=sys.stderr)

    if new_iss == iss_text:
        print("[regen] no changes", file=sys.stderr)
        return 0

    if args.check:
        print("[regen] regeneration would modify the file (use without --check to write)", file=sys.stderr)
        return 1

    iss_path.write_text(new_iss, encoding="utf-8")
    print(f"[regen] wrote {iss_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
