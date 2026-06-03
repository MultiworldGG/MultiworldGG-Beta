# MultiworldGG fuzz image

A minimal, hardened container that fuzzes **one** untrusted MultiworldGG world
and scans its wheel. It is the single-world engine behind the Karen bot's
`repository_dispatch: karen-fuzz` flow (`src/fuzz/runner.ts` builds the
`docker run` and reads `/out/result.json` back).

Everything the run needs is baked into the image — the harness
(`fuzz_bootstrap.py`, `karen_review.py`) is **pinned**, never fetched from a
mutable branch at runtime — so the only moving parts are the world wheel and the
two upstream repos (core + fuzzer) that the run script clones at well-known refs.

## What it does (per invocation)

Driven entirely by env vars, under `/work` (writable tmpfs), writing results to
`/out`:

1. **Download** `FUZZ_WHEEL_URL` to `/work` and **verify** its SHA-256 equals
   `FUZZ_WHEEL_SHA256`. Mismatch ⇒ fail fast (`result.json.scan.sha256:"mismatch"`,
   non-zero `exit_code`).
2. **Extract** the wheel (a zip) to `/work/extracted` with a path-traversal guard.
3. **Scan** the extracted dir with the pinned `karen_review.py --world-dir`
   (`size_sanity`, `no_rom_files`, `no_network_at_import`, `bandit`, `pip_audit`)
   ⇒ `/out/scan.json`; plus `ruff check --output-format json` ⇒ `/out/ruff.json`
   (both advisory, never abort the run).
4. **Clone** core (`MWGG_CORE_REPO@MWGG_CORE_REF`, shallow) into `/work/core`,
   `uv venv`, install `requirements.txt` + the candidate wheel.
5. **Fetch** the upstream fuzzer (`FUZZER_REPO@FUZZER_REF`) `fuzz.py` and
   `sed`-inject the pinned `fuzz_bootstrap.py` immediately before its
   `from worlds import` line (anchored on that line — never a line number), then
   run `timeout <wall> python fuzz.py -r RUNS -t TIMEOUT -g SLUG -j THREADS -n YAMLS`.
6. **Classify** `fuzz_output/report.json` into `pass` / `warn` / `fail` using the
   *same* rules as the legacy `scripts/fuzz_worlds.sh` (`CLASSIFY_JQ`): a non-ROM
   failure or any timeout past 50% ⇒ `fail`; a clean generation ⇒ `pass`;
   everything else (all-`ignored`, ROM/output failures from a missing base ROM on
   CI) ⇒ `warn`.
7. **Write** `/out/result.json` (schema below). A trap guarantees a parseable
   `result.json` is written on *every* exit path — sha mismatch, clone failure,
   wall-clock kill, or an unexpected crash.

## Inputs (environment variables)

| Var | Required | Default | Meaning |
| --- | :---: | --- | --- |
| `FUZZ_SLUG` | ✅ | — | World slug, e.g. `hk`. Must be `[a-z0-9_-]+`. |
| `FUZZ_WHEEL_URL` | ✅ | — | `https://…​.whl` to fuzz. |
| `FUZZ_WHEEL_SHA256` | ✅ | — | 64-hex expected digest of the wheel. |
| `FUZZ_RUNS` | | `50` | Fuzzer `-r`. |
| `FUZZ_TIMEOUT` | | `30` | Fuzzer `-t` (per-generation seconds). |
| `FUZZ_YAMLS` | | `1-10` | Fuzzer `-n` range. |
| `FUZZ_THREADS` | | `10` | Fuzzer `-j`. |
| `MWGG_CORE_REPO` | ✅ | — | `owner/name` of MultiworldGG core. |
| `MWGG_CORE_REF` | ✅ | — | Branch/tag/SHA of core. |
| `FUZZER_REPO` | ✅ | — | `owner/name` of the Eijebong fuzzer. |
| `FUZZER_REF` | ✅ | — | Branch/tag/SHA of the fuzzer. |
| `FUZZ_WALL_SECONDS` | | `1080` | Hard wall for `fuzz.py`. Keep below the bot's outer wall (1200s) so the container exits and writes `result.json` itself. |
| `FUZZ_SIZE_CAP_MB` | | `250` | `size_sanity` cap. |

The bot also sets `KIVY_NO_ARGS=1`, `SKIP_ALL_INSTALLS=1`, `MALLOC_ARENA_MAX=2`
(also defaulted in the image).

## Outputs (`/out`)

- **`result.json`** — the contract the bot reads (schema below). Always written.
- **`scan.json`** — full `karen_review` summary (`{overall, worlds:[…]}`).
- **`ruff.json`** — raw `ruff` findings array (advisory).
- **`report.json`** — the fuzzer's raw report, copied out for debugging (when one
  was produced).

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
    "pip_audit": "pass | warn | fail | skip | missing",
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
  exits `0` with `status:"fail"`. Non-zero exits are reserved for
  download/verify/clone/setup failures and wall-clock kills (`124`/`137`).
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

## Local smoke test

Run exactly as the bot does — read-only root, `/tmp` + `/work` tmpfs, only `/out`
bind-mounted rw, dropped caps, non-root user:

```sh
mkdir -p /tmp/fuzz-out

docker run --rm \
  --user 65532:65532 \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=512m \
  --tmpfs /work:rw,nosuid,size=4g \
  -v /tmp/fuzz-out:/out:rw \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --pids-limit 512 \
  --cpus 2 --memory 4g --memory-swap 4g \
  --network bridge \
  -e FUZZ_SLUG=hk \
  -e FUZZ_WHEEL_URL='https://github.com/<org>/<repo>/releases/download/<tag>/hk-<ver>.whl' \
  -e FUZZ_WHEEL_SHA256='<64-hex sha256 of that wheel>' \
  -e FUZZ_RUNS=10 \
  -e FUZZ_TIMEOUT=30 \
  -e FUZZ_YAMLS=1-5 \
  -e FUZZ_THREADS=4 \
  -e MWGG_CORE_REPO=MultiworldGG/MultiworldGG \
  -e MWGG_CORE_REF=main \
  -e FUZZER_REPO=Eijebong/Archipelago-fuzzer \
  -e FUZZER_REF=main \
  multiworldgg-fuzz

jq . /tmp/fuzz-out/result.json
```

To exercise the **fail-fast** path without a real wheel, point `FUZZ_WHEEL_URL`
at any reachable `.whl` and pass a deliberately wrong `FUZZ_WHEEL_SHA256`; the run
should exit non-zero with `result.json.scan.sha256 == "mismatch"`.

## Hardening summary

- Distroless-ish `python:3.13-slim`; only `git`, `curl`, `jq`, `ca-certificates`
  and the Python audit tooling (`uv bandit pip-audit ruff jsonschema`) added.
- Runs as uid/gid **65532** with `--cap-drop ALL`, `--security-opt
  no-new-privileges`, a read-only root FS, and a `pids-limit`.
- Untrusted world code only ever executes inside the run's own `/work` venv,
  behind the fuzzer; it never runs during the scan (the scan is static —
  `karen_review` AST-inspects, it does not import the world).
- The harness is pinned into the image. The only network at runtime is the wheel
  download and the two pinned-ref clones/fetches.
- Every cache/`$HOME` write is redirected to `/work`, so the read-only root FS is
  never written.
