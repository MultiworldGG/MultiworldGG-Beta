"""Check which released wheels (pinned in the Index) lack the mwgg.client hook.

For each candidate world: read MultiworldGG-Index/worlds/<world>.json -> module_location,
open the wheel over HTTP via range requests, and report whether its
entry_points.txt declares [mwgg.client].
"""
import io
import json
import sys
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

INDEX = Path(r"C:\Users\Lindsay\source\repos\MultiworldGG-Index")

CANDIDATES = """
adventure ahit albw am2r animal_well apquest banjo_tooie bfbb checksfinder
civ_6 diddy_kong_racing dontstarvetogether factorio factorio_saws hades
hitman_woa kh1 kh2 ladx_beta lego_star_wars_tcs luigismansion
mario_kart_double_dash megamix messenger metroidprime minecraft mmbn3 oot
portal2 rabi_ribi rac2 rac3 sc2 simpsonshitnrun sly1 sms srb2 ss tp tracker
trackmania ttyd tww undertale wargroove wargroove2 zillion
""".split()


class HTTPRangeFile(io.RawIOBase):
    """Minimal seekable read-only file backed by HTTP Range requests."""

    def __init__(self, url):
        head = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(head, timeout=30) as r:
            self.url = r.geturl()  # resolved past redirects
            self.length = int(r.headers["Content-Length"])
        self.pos = 0

    def seekable(self):
        return True

    def seek(self, off, whence=0):
        self.pos = {0: off, 1: self.pos + off, 2: self.length + off}[whence]
        return self.pos

    def tell(self):
        return self.pos

    def read(self, size=-1):
        end = self.length - 1 if size is None or size < 0 else min(self.pos + size - 1, self.length - 1)
        if self.pos > end:
            return b""
        req = urllib.request.Request(self.url, headers={"Range": f"bytes={self.pos}-{end}"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        self.pos += len(data)
        return data


def module_location(world):
    p = INDEX / "worlds" / f"{world}.json"
    if not p.is_file():
        return None
    url = json.loads(p.read_text(encoding="utf-8")).get("module_location")
    return url.split("#", 1)[0] if url else None


def check(world):
    try:
        url = module_location(world)
        if not url:
            return world, "NO-INDEX-URL"
        if not url.endswith(".whl"):
            return world, f"NOT-A-WHEEL ({url.rsplit('/', 1)[-1]})"
        z = zipfile.ZipFile(HTTPRangeFile(url))
        eps = [n for n in z.namelist() if n.endswith("entry_points.txt")]
        if not eps:
            return world, "UNHOOKED"
        has = any("mwgg.client" in z.read(n).decode("utf-8", "ignore") for n in eps)
        return world, ("HOOKED" if has else "UNHOOKED")
    except Exception as e:  # noqa: BLE001
        return world, f"ERROR {type(e).__name__}: {e}"


def main():
    results = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        for world, status in ex.map(check, CANDIDATES):
            results[world] = status
            print(f"  {world:24} {status}", flush=True)

    rebuild = sorted(w for w, s in results.items() if s == "UNHOOKED")
    hooked = sorted(w for w, s in results.items() if s == "HOOKED")
    other = sorted((w, s) for w, s in results.items() if s not in ("UNHOOKED", "HOOKED"))

    print("\n" + "=" * 60)
    print(f"REBUILD (released wheel unhooked) - {len(rebuild)}:")
    print("  " + " ".join(rebuild))
    print(f"\nALREADY HOOKED (skip) - {len(hooked)}:")
    print("  " + " ".join(hooked))
    if other:
        print(f"\nNEEDS A LOOK - {len(other)}:")
        for w, s in other:
            print(f"  {w:24} {s}")


if __name__ == "__main__":
    sys.exit(main())
