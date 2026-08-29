#!/usr/bin/env python3
"""
Regenerate the autogen regions of src/inno_setup.iss from the published
mwgg_igdb game-index variant package.

Three regions are managed:
  - in_client       : `#define InClientDescriptions "..."` near the top
  - components      : the entire `[Components]` block
  - wheel_downloads : per-world `[Files]` `download`-flag entries that fetch
                      each world's wheel into `{app}\\wheel_cache` at install
                      time (Inno 6.5.0+); source and hash come from the
                      manifest's `module_location` release-asset wheel URL

Each region is delimited by `BEGIN AUTOGEN: <name>` / `END AUTOGEN: <name>`
markers; everything outside the markers is left untouched.

Disk-size policy (ExtraDiskSpaceRequired is bytes):
  - Prefer `disk_space_mb` from the manifest (ceil-MB of the wheel, stamped by
    gen-pymod-release per-world CI), converted to bytes. Legacy `disk_space_kb`
    inputs are consumed verbatim as bytes, matching the values they seeded.
  - Fall back to the value parsed out of the existing iss file for worlds that
    haven't yet rolled out the gen-pymod-release size step.
  - If both are missing, emit a warning and use 0.

In-client policy:
  - Worlds flagged `in_client` (manifest `flags`) are rendered into the
    InClientDescriptions define (bolded as free games in the installer's
    component list). The live index currently carries no `flags` field, so
    when no world is flagged the existing region body is preserved verbatim
    with a warning instead of being blanked.

Wheel-size (ExternalSize) policy:
  - Prefer `wheel_size` from the manifest/`--from-json` input if present.
  - Else HEAD the wheel URL for Content-Length (skipped entirely, no network,
    when `--from-json` is given).
  - Fall back to the value parsed out of the existing iss file, else warn and
    use 0.

The script is idempotent: same input -> byte-identical output.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
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


def _slug_from_component_name(name: str) -> str:
    """Inverse of _component_name: strip the leading `_` from `_<digits>...`."""
    if len(name) >= 2 and name[0] == "_" and name[1].isdigit():
        return name[1:]
    return name


def parse_existing_components(iss_text: str) -> dict[str, dict[str, Any]]:
    """Parse the current `[Components]` autogen body to build a fallback table.

    Keyed by world slug (not by mangled Inno component Name), so callers can
    look up by slug regardless of whether the existing iss line was emitted
    with the mangled `_2048` form or the raw form.

    Returns: { slug: { "description": ..., "disk_space_kb": int } }
    """
    out: dict[str, dict[str, Any]] = {}
    region = _find_region(iss_text, "components")
    if region is None:
        return out
    for m in COMPONENT_LINE.finditer(region):
        slug = _slug_from_component_name(m["slug"])
        out[slug] = {
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


def _manifest_game(manifest: dict[str, Any]) -> str | None:
    """Display name; the live index renamed `game` to `game_name`, accept both."""
    return manifest.get("game_name") or manifest.get("game")


def _manifest_disk_space(manifest: dict[str, Any]) -> int | None:
    """ExtraDiskSpaceRequired bytes from the manifest, or None.

    The live index stamps `disk_space_mb` (ceil-MB of the wheel); the original
    `disk_space_kb` key never made it into any live manifest but is kept for
    fixtures, consumed verbatim as bytes like the iss values it mirrors.
    """
    if "disk_space_mb" in manifest:
        return int(manifest["disk_space_mb"]) * 1024 * 1024
    if "disk_space_kb" in manifest:
        return int(manifest["disk_space_kb"])
    return None


def _format_kb(value: int) -> str:
    """Render an int as Inno Setup's underscore-separated thousands grouping."""
    s = str(value)
    out = []
    while len(s) > 3:
        out.append(s[-3:])
        s = s[:-3]
    out.append(s)
    return "_".join(reversed(out))


def _component_name(slug: str) -> str:
    """Transform a world slug into a valid Inno Setup component Name.

    Inno requires Name: to be alphanumeric/underscore/slash and not start with
    a digit. Any slug that starts with a digit is prefixed with '_' so e.g.
    '2048' becomes '_2048'. The python module reference (worlds.<slug>) is
    unchanged - only the installer-side identifier is mangled.
    """
    if slug and slug[0].isdigit():
        return f"_{slug}"
    return slug


def render_components(
    games: dict[str, dict[str, Any]],
    fallback: dict[str, dict[str, Any]],
) -> str:
    lines: list[str] = []
    for slug in sorted(games.keys()):
        manifest = games[slug]
        description = _manifest_game(manifest) or fallback.get(slug, {}).get("description") or slug
        size = _manifest_disk_space(manifest)
        if size is None:
            fb = fallback.get(slug, {})
            if "disk_space_kb" in fb:
                size = fb["disk_space_kb"]
            else:
                print(
                    f"[regen] warning: no disk-space value for '{slug}' (manifest "
                    f"missing disk_space_mb, no fallback in current iss); using 0",
                    file=sys.stderr,
                )
                size = 0
        size_text = _format_kb(int(size))
        # Escape any embedded quotes in the description, defensively.
        desc = description.replace('"', '""')
        lines.append(
            f'Name: "{_component_name(slug)}"; Description: "{desc}"; '
            f'ExtraDiskSpaceRequired: {size_text}'
        )
    return "\n".join(lines) + "\n"


def render_in_client_descriptions(
    games: dict[str, dict[str, Any]],
    existing_body: str | None,
) -> str:
    in_client_descs = sorted(
        _manifest_game(manifest) or slug
        for slug, manifest in games.items()
        if "in_client" in (manifest.get("flags") or [])
    )
    if not in_client_descs and existing_body is not None:
        print(
            "[regen] warning: no world carries an 'in_client' flag (the live index "
            "schema has no `flags` field); preserving the existing in_client region",
            file=sys.stderr,
        )
        return existing_body
    # TStringList.CommaText treats both whitespace and commas as separators
    # unless an item is double-quoted. Quote every item so descriptions like
    # "A Hat in Time" round-trip as a single entry. Embedded double-quotes are
    # escaped by doubling per Delphi convention. The whole iss-side string is
    # single-quoted in the Pascal code, so double-quotes don't need escaping
    # at the iss preprocessor level.
    quoted = [f'""{d.replace(chr(34), chr(34) * 2)}""' for d in in_client_descs]
    joined = ",".join(quoted)
    return f'#define InClientDescriptions "{joined}"\n'


# ---------------------------- wheel_downloads --------------------------------

# module_location like <base_url>.whl#sha256=<64-hex>; legacy `git+...@ref`
# entries and any URL missing the sha fragment don't match and are skipped.
WHEEL_LOCATION_PATTERN = re.compile(r"^(?P<base_url>[^#]+\.whl)#sha256=(?P<sha256>[0-9a-fA-F]{64})$")

# Matches a rendered wheel_downloads [Files] line, for the ExternalSize fallback table.
WHEEL_DOWNLOAD_LINE = re.compile(
    r'^\s*Source:\s*"(?P<url>[^"]+)";\s*DestDir:\s*"\{app\}\\wheel_cache";\s*'
    r'DestName:\s*"(?P<destname>[^"]+)";\s*ExternalSize:\s*(?P<size>\d+);\s*'
    r'Hash:\s*"(?P<hash>[0-9a-fA-F]+)";\s*Components:\s*(?P<slug>\S+);\s*'
    r'Flags:\s*external download ignoreversion\s*$',
    re.MULTILINE,
)


def parse_existing_wheel_sizes(iss_text: str) -> dict[str, int]:
    """Parse the current `wheel_downloads` region for a slug -> ExternalSize fallback table."""
    out: dict[str, int] = {}
    region = _find_region(iss_text, "wheel_downloads")
    if region is None:
        return out
    for m in WHEEL_DOWNLOAD_LINE.finditer(region):
        out[_slug_from_component_name(m["slug"])] = int(m["size"])
    return out


def _parse_wheel_location(location: Any) -> tuple[str, str] | None:
    """Split a `module_location` wheel URL into (url_without_fragment, sha256_hex), or None."""
    if not isinstance(location, str):
        return None
    m = WHEEL_LOCATION_PATTERN.match(location)
    if not m:
        return None
    return m["base_url"], m["sha256"].lower()


def _fetch_content_length(url: str) -> int | None:
    """HEAD `url` (following redirects, e.g. GitHub's 302 to a signed S3 host) for its size."""
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            length = resp.headers.get("Content-Length")
    except (urllib.error.URLError, OSError) as e:
        print(f"[regen] warning: HEAD request failed for {url}: {e}", file=sys.stderr)
        return None
    return int(length) if length else None


def resolve_wheel_size(
    slug: str, manifest: dict[str, Any], url: str, fallback: dict[str, int], use_network: bool,
) -> int:
    if "wheel_size" in manifest:
        return int(manifest["wheel_size"])
    if use_network:
        size = _fetch_content_length(url)
        if size is not None:
            return size
    if slug in fallback:
        return fallback[slug]
    print(f"[regen] warning: no size available for wheel '{slug}' ({url}); using 0", file=sys.stderr)
    return 0


def render_wheel_downloads(
    games: dict[str, dict[str, Any]],
    fallback_sizes: dict[str, int],
    use_network: bool,
) -> str:
    lines: list[str] = []
    skipped: list[str] = []
    for slug in sorted(games.keys()):
        manifest = games[slug]
        parsed = _parse_wheel_location(manifest.get("module_location"))
        if parsed is None:
            skipped.append(slug)
            continue
        base_url, sha256_hex = parsed
        dest_name = base_url.rsplit("/", 1)[-1]
        size = resolve_wheel_size(slug, manifest, base_url, fallback_sizes, use_network)
        lines.append(
            f'Source: "{base_url}"; DestDir: "{{app}}\\wheel_cache"; DestName: "{dest_name}"; '
            f'ExternalSize: {size}; Hash: "{sha256_hex}"; '
            f'Components: {_component_name(slug)}; Flags: external download ignoreversion'
        )
    if skipped:
        print(
            f"[regen] warning: skipped {len(skipped)} world(s) with no downloadable wheel "
            f"module_location (missing, non-wheel, or unhashed): {', '.join(skipped)}",
            file=sys.stderr,
        )
    return "\n".join(lines) + "\n" if lines else "\n"


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
        new_desc = _manifest_game(new) or slug
        new_size = _manifest_disk_space(new)
        if new_size is None:
            new_size = old["disk_space_kb"]
        if old["description"] != new_desc or old["disk_space_kb"] != new_size:
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
        help="Read the games dict from a JSON file instead of mwgg_igdb, and skip all "
             "network calls (wheel sizes come from 'wheel_size' or the iss fallback). "
             "Schema: { '<slug>': { 'game_name': str (or legacy 'game'), 'flags': [..], "
             "'disk_space_mb': int (or legacy 'disk_space_kb' bytes), "
             "'module_location': str, 'wheel_size': int } }",
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
        use_network = False
    else:
        games = load_index(args.variant)
        use_network = True

    fallback = parse_existing_components(iss_text)
    fallback_wheel_sizes = parse_existing_wheel_sizes(iss_text)

    new_iss = iss_text
    new_iss = replace_region(new_iss, "components", render_components(games, fallback))
    new_iss = replace_region(
        new_iss, "in_client",
        render_in_client_descriptions(games, _find_region(iss_text, "in_client")),
    )
    new_iss = replace_region(
        new_iss, "wheel_downloads", render_wheel_downloads(games, fallback_wheel_sizes, use_network),
    )

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
