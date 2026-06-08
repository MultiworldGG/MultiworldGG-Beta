# MultiworldGG fuzz image

A minimal, hardened container that fuzzes **one** untrusted MultiworldGG world
and scans its wheel. It is the single-world engine behind the Karen bot's
`repository_dispatch: karen-fuzz` flow (`src/fuzz/runner.ts` builds the
`docker run` and reads `/out/result.json` back).

Everything the run needs is baked into the image — the harness
(`fuzz_bootstrap.py`, `karen_review.py`) plus core (with its `.venv`) and the
fuzzer's `fuzz.py` are all **pinned** at build time, never fetched at runtime — so
the only moving part is the world wheel, which the trusted bot bind-mounts
read-only at `/in`. The container itself runs `--network none`.

## What it does (per invocation)

Driven by `FUZZ_*` env vars plus the wheel bind-mounted at `/in` (under its real
PEP 427 filename — the bot mounts exactly one `.whl` there), under `/work`
(writable tmpfs), writing results to `/out`:

1. **Stage** the bind-mounted wheel (the single `/in/*.whl`) to `/work`
   (preserving its filename — `uv pip install` parses it) and
   **re-verify** its SHA-256 equals `FUZZ_WHEEL_SHA256` — the bot already verified
   before mounting, so this is defense in depth. Mismatch ⇒ fail fast
   (`result.json.scan.sha256:"mismatch"`, `exit_code:3`).
2. **Extract** the wheel (a zip) to `/work/extracted` with a path-traversal guard.
3. **Scan** the extracted dir with the pinned `karen_review.py --world-dir`
   (`size_sanity`, `no_rom_files`, `no_network_at_import`, `bandit`) ⇒
   `/out/scan.json`; plus `ruff check --output-format json` ⇒ `/out/ruff.json`
   (both advisory, never abort the run). `pip_audit` is **not** run: it queries
   PyPI's advisory DB online and the container is `--network none`.
4. **Stage** the baked core (`/opt/fuzz/core`, including its relocatable `.venv`)
   into `/work/core` with `cp -a`, then install the candidate wheel into that venv
   with `uv pip install --offline --no-deps`. No clone, no `uv venv`, no network —
   core and its `requirements.txt` were installed into the venv at build time.
5. **Copy** the baked `fuzz.py` (`/opt/fuzz/fuzz.py`) into the core and
   `sed`-inject the pinned `fuzz_bootstrap.py` immediately before its
   `from worlds import` line (anchored on that line — never a line number), then
   run `timeout <wall> python fuzz.py -r RUNS -t TIMEOUT -g SLUG -j THREADS -n YAMLS`.
6. **Classify** `fuzz_output/report.json` into `pass` / `warn` / `fail` using the
   *same* rules as the legacy `scripts/fuzz_worlds.sh` (`CLASSIFY_JQ`): a non-ROM
   failure or any timeout past 50% ⇒ `fail`; a clean generation ⇒ `pass`;
   everything else (all-`ignored`, ROM/output failures from a missing base ROM on
   CI) ⇒ `warn`.
7. **Write** `/out/result.json` (schema below). A trap guarantees a parseable
   `result.json` is written on *every* exit path — sha mismatch, offline
   wheel-install failure, wall-clock kill, or an unexpected crash.

## Inputs

The world wheel is **not** an env var: the trusted bot bind-mounts it read-only at
`/in` under its real `.whl` filename (the container is `--network none` and
fetches nothing; `uv` parses that filename, so it can't be a fixed `world.whl`).
Core, its
venv, and `fuzz.py` are baked into the image at build time — see [Build](#build) —
not passed at runtime. The remaining job parameters arrive as env vars:

| Var | Required | Default | Meaning |
| --- | :---: | --- | --- |
| `FUZZ_SLUG` | ✅ | — | World slug, e.g. `hk`. Must be `[a-z0-9_-]+`. |
| `FUZZ_WHEEL_SHA256` | ✅ | — | 64-hex expected digest, **re-verified in-container** against the bytes of the wheel mounted at `/in`. |
| `FUZZ_RUNS` | | `50` | Fuzzer `-r`. |
| `FUZZ_TIMEOUT` | | `30` | Fuzzer `-t` (per-generation seconds). |
| `FUZZ_YAMLS` | | `1-10` | Fuzzer `-n` range. |
| `FUZZ_THREADS` | | `10` | Fuzzer `-j`. |
| `FUZZ_WALL_SECONDS` | | `1080` | Hard wall for `fuzz.py`. Keep below the bot's outer wall (1200s) so the container exits and writes `result.json` itself. |
| `FUZZ_SIZE_CAP_MB` | | `250` | `size_sanity` cap. |
| `FUZZ_DEBUG` | | (off) | Truthy (`1`/`true`/`yes`/`on`) ⇒ also copy the full `combined.log` and the fuzzer's `fuzz_output/` worker dumps into `/out`. |

Core and fuzzer refs are **build** inputs, not runtime env vars: `MWGG_CORE_REPO`,
`MWGG_CORE_REF`, `FUZZER_REPO`, `FUZZER_REF` are `ARG`s baked at build time (see
[Build](#build)).

The bot also sets `KIVY_NO_ARGS=1`, `SKIP_ALL_INSTALLS=1`, `MALLOC_ARENA_MAX=2`
(also defaulted in the image).

## Outputs (`/out`)

- **`result.json`** — the contract the bot reads (schema below). Always written.
- **`scan.json`** — full `karen_review` summary (`{overall, worlds:[…]}`).
- **`ruff.json`** — raw `ruff` findings array (advisory).
- **`report.json`** — the fuzzer's raw report, copied out for debugging (when one
  was produced).
- **`combined.log`** — the FULL run log (only with `FUZZ_DEBUG`; `result.json`
  carries just its last ~4KB). Written on every exit path, including crashes.
- **`fuzz_output/`** — the fuzzer's per-generation worker dumps: tracebacks and
  the failing YAMLs (only with `FUZZ_DEBUG`). This is where a generation's *real*
  failure reason lives — it never reaches `result.json`.

### `result.json` schema

```json
{
  "slug": "hk",
  "status": "pass | warn | fail",
  "stats": {
    "success": 0,
    "failure": 0,
    "timeout": 0,
    "ignored": 0,
    "total": 0
  },
  "scan": {
    "bandit": "pass | warn | fail | skip | missing",
    "pip_audit": "skipped",
    "size_sanity": "pass | warn | fail | skip | missing",
    "no_rom_files": "pass | warn | fail | skip | missing",
    "no_network_at_import": "pass | warn | fail | skip | missing",
    "ruff": "captured | missing"
  },
  "exit_code": 0,
  "log_tail": "…last ~4 KB of the combined log…"
}
```

On a **SHA mismatch** the object is shaped `{slug, status:"fail",
scan:{sha256:"mismatch"}, exit_code:3, log_tail}` (stats may be zeroed) — the
distinguishing field is `scan.sha256`.

Contract notes that match `src/fuzz/runner.ts`:

- **`exit_code`** mirrors the process exit. `0` means the harness ran to
  completion; the *verdict* lives in `status`. Any non-zero `exit_code` makes the
  bot force the world to `fail` regardless of `status` (a wheel/setup failure
  invalidates the verdict).
- A classifier `fail` (a real world failure) is still a *completed* run, so it
  exits `0` with `status:"fail"`. Non-zero exits are reserved for wheel-verify,
  extraction, or offline-setup failures and wall-clock kills (`124`/`137`).
- `stats` values are all finite numbers; the bot drops any non-numeric field.
- `scan`/`log_tail` are advisory; the bot surfaces them in the PR comment.

## Build

```sh
docker build -t multiworldgg-fuzz .
```

The build vendors `karen_review.py` and `fuzz_bootstrap.py` from this directory
(they are copied here from the Index repo's `scripts/`). Re-copy them when the
upstream harness changes:

```sh
cp ../../../../MultiworldGG-Index/scripts/karen_review.py .
cp ../../../../MultiworldGG-Index/scripts/fuzz_bootstrap.py .
docker build -t multiworldgg-fuzz .
```

Core (with its `.venv`) and the fuzzer's `fuzz.py` are cloned/fetched at **build**
time and baked in via build args — the build has network, the runtime does not.
They default to the values below (the `ARG`s in the Dockerfile); override to pin a
different ref. Per the design, core need not be fresh every run — rebuild to
update it.

```sh
docker build -t multiworldgg-fuzz \
  --build-arg MWGG_CORE_REPO=MultiworldGG/MultiworldGG-Beta \
  --build-arg MWGG_CORE_REF=main \
  --build-arg FUZZER_REPO=Eijebong/Archipelago-fuzzer \
  --build-arg FUZZER_REF=main \
  .
```

## Local smoke test

Run exactly as the bot does — `--network none`, read-only root, `/tmp` + `/work`
tmpfs, the wheel bind-mounted read-only at `/in` and `/out` bind-mounted rw,
dropped caps, non-root user:

```sh
work="$(mktemp -d)"
mkdir -p "$work/in" "$work/out"

# Drop the wheel under its REAL filename (the run script globs /in/*.whl and uv
# parses that name — a fixed world.whl is rejected). Exactly one .whl at /in.
cp /path/to/hk-<ver>.whl "$work/in/"
sha="$(sha256sum "$work"/in/*.whl | awk '{print $1}')"

# The container runs as uid 65532 and writes /out/result.json; the bot chmods the
# out dir 0777 for exactly this reason, so do the same (or run docker as root).
chmod 777 "$work/out"

docker run --rm \
  --user 65532:65532 \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=512m,mode=1777 \
  --tmpfs /work:rw,nosuid,size=4g,mode=1777 \
  -v "$work/in:/in:ro" \
  -v "$work/out:/out:rw" \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --pids-limit 512 \
  --cpus 2 --memory 4g --memory-swap 4g \
  --ulimit nofile=4096:4096 \
  --network none \
  -e FUZZ_SLUG=hk \
  -e FUZZ_WHEEL_SHA256="$sha" \
  -e FUZZ_RUNS=10 \
  -e FUZZ_TIMEOUT=30 \
  -e FUZZ_YAMLS=1-5 \
  -e FUZZ_THREADS=4 \
  multiworldgg-fuzz

jq . "$work/out/result.json"
```

The `mode=1777` on the tmpfs mounts and `chmod 777` on the out dir are not
cosmetic: with explicit tmpfs options Docker skips its default mode, so the tmpfs
root would otherwise be `0755 root` and the `--user 65532` process could not
create `/work/.cache`; a `0755` out dir would likewise block `/out/result.json`,
masking the container's real exit behind a "no result.json".

To exercise the **fail-fast** path, drop any `.whl` in `$work/in/` and pass a
deliberately wrong `FUZZ_WHEEL_SHA256`; the run exits `3` with
`result.json.scan.sha256 == "mismatch"` (the sha is checked on the bytes, before
the install, so the filename doesn't matter for this path).

## Hardening summary

- Distroless-ish `python:3.13-slim`; only `git`, `curl`, `jq`, `ca-certificates`
  and the Python audit tooling (`uv bandit pip-audit ruff jsonschema`) added.
- Runs as uid/gid **65532** with `--cap-drop ALL`, `--security-opt
  no-new-privileges`, a read-only root FS, `--network none`, and a `pids-limit`.
- Untrusted world code only ever executes inside the run's own `/work` venv,
  behind the fuzzer; it never runs during the scan (the scan is static —
  `karen_review` AST-inspects, it does not import the world).
- The harness **and** the pinned core (with its venv) + fuzzer `fuzz.py` are baked
  into the image at build time, so the container needs **zero** network at runtime
  (`--network none`). The only runtime input is the wheel, bind-mounted read-only
  at `/in` by the trusted bot.
- Every cache/`$HOME` write is redirected to `/work`, so the read-only root FS is
  never written.
