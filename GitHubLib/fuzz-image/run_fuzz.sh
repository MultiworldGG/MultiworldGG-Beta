#!/usr/bin/env bash
# Single-world fuzz + scan, run inside the hardened image (see Dockerfile).
#
# A SINGLE-WORLD port of the Index repo's scripts/fuzz_worlds.sh, driven by env
# vars instead of a karen-targets.txt list. The bot (src/fuzz/runner.ts) bind-
# mounts the wheel at /in (ro) and /out (rw); /tmp and /work are writable tmpfs,
# everything else (incl. the baked core under /opt/fuzz) is read-only. The
# container runs with NO network.
#
# Inputs:
#   /in/<name>.whl     the wheel to fuzz (its REAL PEP 427 filename — NOT a fixed
#                      name; uv parses the filename and rejects e.g. world.whl),
#                      bind-mounted READ-ONLY by the bot. Exactly one .whl at /in.
#   FUZZ_SLUG          world slug, e.g. "hk"            (required)
#   FUZZ_WHEEL_SHA256  64-hex expected digest of wheel (required; re-verified here)
#   FUZZ_RUNS          fuzzer -r                        (default 50)
#   FUZZ_TIMEOUT       fuzzer -t per-generation secs    (default 30)
#   FUZZ_YAMLS         fuzzer -n range, e.g. "1-10"      (default 1-10)
#   FUZZ_THREADS       fuzzer -j                         (default 10)
#   FUZZ_WALL_SECONDS  hard wall for fuzz.py             (default 1080)
#   FUZZ_SIZE_CAP_MB   size_sanity cap                   (default 250)
#
# Core, its venv, and fuzz.py are BAKED into the image (pinned at build) under
# /opt/fuzz; the container fetches nothing at runtime.
#
# Outputs (all under /out):
#   result.json  the contract the bot reads back (schema in README.md)
#   scan.json    karen_review --output-summary (wheel-targeted deep checks)
#   ruff.json    `ruff check --output-format json` of the extracted wheel
#
# Exit code mirrors result.json.exit_code: 0 only on a clean pass/warn run; any
# setup/verification failure is non-zero, which the bot treats as a hard fail.

set -euo pipefail

# --- Fixed layout. /work + /out are the only writable mounts; never touch $HOME
# defaults that might resolve to the read-only root.
WORK=/work
OUT=/out
EXTRACTED="${WORK}/extracted"
CORE="${WORK}/core"
HARNESS_DIR=/opt/fuzz
LOG="${WORK}/combined.log"

SLUG="${FUZZ_SLUG:-}"
WHEEL_IN=""                              # resolved to the single /in/*.whl in run()
WHEEL_SHA256="$(printf '%s' "${FUZZ_WHEEL_SHA256:-}" | tr '[:upper:]' '[:lower:]')"
RUNS="${FUZZ_RUNS:-50}"
TIMEOUT_S="${FUZZ_TIMEOUT:-30}"
YAMLS="${FUZZ_YAMLS:-1-10}"
THREADS="${FUZZ_THREADS:-10}"
BAKED_CORE=/opt/fuzz/core                # core + its relocatable .venv, baked at build
BAKED_FUZZER=/opt/fuzz/fuzz.py           # pinned fuzzer entrypoint, baked at build
WALL_SECONDS="${FUZZ_WALL_SECONDS:-1080}"
SIZE_CAP_MB="${FUZZ_SIZE_CAP_MB:-250}"
# Opt-in debug: when truthy, persist the FULL combined log and the fuzzer's
# per-generation worker dumps (fuzz_output/) into /out so a failing run leaves
# diagnostics behind. The bot also keeps the per-job dir when this is on.
DEBUG="${FUZZ_DEBUG:-}"

# Verdict state shared between run() and the EXIT trap. The trap is the single
# writer of /out/result.json on ANY exit path, so partial/crashed runs still
# leave the bot something parseable.
STATUS="fail"
EXIT_CODE=1
STATS_JSON='{"success":0,"failure":0,"timeout":0,"ignored":0,"total":0}'
SCAN_JSON='{}'
RESULT_WRITTEN=0

mkdir -p "${OUT}"
# Pre-make the writable caches our env (Dockerfile) points HOME/XDG/uv/pip at, now
# that /work is mounted. Without these, the first tool that writes a cache dies.
mkdir -p "${WORK}/.cache/uv" "${WORK}/.cache/pip" "${WORK}/.config" "${WORK}/.local/share"
: > "${LOG}"

# Mirror everything to the console AND the log file we tail into result.json.
log() { printf '%s\n' "$*" | tee -a "${LOG}" >&2; }

# Read the JSON object emitted by karen_review for a single check's status.
# Args: <check_name>. Echoes "pass"|"warn"|"fail"|"skip"|"missing".
scan_status() {
    local name="$1"
    if [ ! -s "${OUT}/scan.json" ]; then
        printf 'missing'
        return
    fi
    jq -r --arg n "$name" '
        (.worlds[0].checks // []) | map(select(.name == $n)) | (.[0].status // "missing")
    ' "${OUT}/scan.json" 2>/dev/null || printf 'missing'
}

# Last ~4KB of the combined log, JSON-safe. Truncated to the TAIL of the file so a
# noisy run still surfaces its final error.
log_tail_json() {
    if [ -s "${LOG}" ]; then
        tail -c 4096 "${LOG}" | jq -Rs .
    else
        printf '""'
    fi
}

# The ONLY writer of /out/result.json. Idempotent-ish: guarded so the trap won't
# overwrite a richer result the happy path already wrote.
write_result() {
    RESULT_WRITTEN=1
    local ruff_status="missing"
    [ -s "${OUT}/ruff.json" ] && ruff_status="captured"

    jq -n \
        --arg slug "${SLUG:-unknown}" \
        --arg status "${STATUS}" \
        --argjson stats "${STATS_JSON}" \
        --arg bandit "$(scan_status bandit)" \
        --arg pip_audit "skipped" \
        --arg size_sanity "$(scan_status size_sanity)" \
        --arg no_rom_files "$(scan_status no_rom_files)" \
        --arg no_network_at_import "$(scan_status no_network_at_import)" \
        --arg ruff "${ruff_status}" \
        --argjson exit_code "${EXIT_CODE}" \
        --argjson log_tail "$(log_tail_json)" \
        '{
            slug: $slug,
            status: $status,
            stats: $stats,
            scan: {
                bandit: $bandit,
                pip_audit: $pip_audit,
                size_sanity: $size_sanity,
                no_rom_files: $no_rom_files,
                no_network_at_import: $no_network_at_import,
                ruff: $ruff
            },
            exit_code: $exit_code,
            log_tail: $log_tail
        }' > "${OUT}/result.json".tmp 2>>"${LOG}" \
        && mv -f "${OUT}/result.json".tmp "${OUT}/result.json"

    # Last-ditch: if jq itself failed (e.g. a malformed STATS_JSON), hand-write a
    # minimal-but-valid object so the bot never sees a truncated/absent file.
    if [ ! -s "${OUT}/result.json" ]; then
        printf '{"slug":"%s","status":"fail","stats":%s,"scan":{},"exit_code":%s,"log_tail":""}\n' \
            "${SLUG:-unknown}" "${STATS_JSON}" "${EXIT_CODE}" > "${OUT}/result.json" || true
    fi
}

# When FUZZ_DEBUG is truthy, copy the full combined log and the fuzzer's
# per-generation worker dumps (tracebacks + failing YAMLs, written to
# ${CORE}/fuzz_output) into /out. result.json only carries the last ~4KB of the
# log, and worker tracebacks never reach it at all — so this is the only way to
# see WHY a generation (e.g. a ROM world) actually failed. No-op unless enabled;
# best-effort so it never changes the run's verdict/exit code.
persist_debug_artifacts() {
    case "${DEBUG}" in 1|true|TRUE|yes|on) ;; *) return 0 ;; esac
    cp -f "${LOG}" "${OUT}/combined.log" 2>>"${LOG}" || true
    if [ -d "${CORE}/fuzz_output" ]; then
        rm -rf "${OUT}/fuzz_output"
        cp -a "${CORE}/fuzz_output" "${OUT}/fuzz_output" 2>>"${LOG}" || true
    fi
}

# Always leave a parseable result.json behind, whatever killed us (set -e abort,
# `timeout` SIGTERM, OOM bubbling up as a non-zero, ...).
on_exit() {
    local rc=$?
    if [ "${RESULT_WRITTEN}" -eq 0 ]; then
        # Nothing wrote a verdict yet -> crash/abort. Surface the shell's rc.
        EXIT_CODE="${rc}"
        STATUS="fail"
        write_result
    fi
    # Single exit point, so every path (success, die, crash) persists the logs
    # when debug is on — including the no-report crashes that produce die 8.
    persist_debug_artifacts
    exit "${EXIT_CODE}"
}
trap on_exit EXIT

# Fail fast with a written result + the given exit code.
die() {
    local code="$1"; shift
    log "ERROR: $*"
    EXIT_CODE="${code}"
    STATUS="fail"
    write_result
    exit "${EXIT_CODE}"
}

# Same three-state classifier as scripts/fuzz_worlds.sh (kept byte-identical so a
# verdict here matches the legacy multi-world runner). Emits:
#   "<status> <success> <failure> <timeout> <ignored> <rom> <real> <total>"
CLASSIFY_JQ='
  def romlike:
    test("no such file or directory|\\brom\\b|\\.(gba|gbc|gb|sfc|smc|z64|n64|nes|md|gen|iso|bin|pce|nds)([^a-z0-9]|$)"; "i");
  (.stats.success // 0) as $succ
  | (.stats.failure // 0) as $fail
  | (.stats.timeout // 0) as $to
  | (.stats.ignored // 0) as $ign
  | (.stats.total   // 0) as $total
  | [ (.errors // {}) | .[] | to_entries[] | select(.key | test("TimeoutError") | not) ] as $fk
  | ( [ $fk[] | select(.key | romlike)       | (.value | length) ] | add // 0 ) as $rom
  | ( [ $fk[] | select(.key | (romlike|not)) | (.value | length) ] | add // 0 ) as $real
  | ( $to + $real ) as $bad
  | ( if   ($total > 0) and (($bad / $total) > 0.5)                     then "fail"
      elif ($succ > 0) and ($to == 0) and ($real == 0) and ($rom == 0) then "pass"
      else "warn" end ) as $status
  | "\($status) \($succ) \($fail) \($to) \($ign) \($rom) \($real) \($total)"
'

run() {
    # --- Validate required inputs up front; a missing one is an internal dispatch
    # bug, surfaced as a non-zero exit (bot -> hard fail).
    [ -n "${SLUG}" ]        || die 2 "FUZZ_SLUG is required"
    # The bot bind-mounts exactly ONE wheel at /in under its REAL PEP 427 filename
    # (uv pip install parses the filename; a fixed name like world.whl is rejected
    # with "Must have a version"). Resolve it by glob — nullglob so a no-match
    # leaves the array empty, and we guard the count before indexing under set -u.
    shopt -s nullglob
    local in_wheels=( /in/*.whl )
    shopt -u nullglob
    [ "${#in_wheels[@]}" -eq 1 ] || die 2 "expected exactly one .whl at /in, found ${#in_wheels[@]}"
    WHEEL_IN="${in_wheels[0]}"
    [ -s "${WHEEL_IN}" ]    || die 2 "wheel not bind-mounted at /in"
    [ -n "${WHEEL_SHA256}" ]|| die 2 "FUZZ_WHEEL_SHA256 is required"
    [ -d "${BAKED_CORE}" ]  || die 2 "baked core missing at ${BAKED_CORE}"
    [ -s "${BAKED_FUZZER}" ]|| die 2 "baked fuzz.py missing at ${BAKED_FUZZER}"
    case "${SLUG}" in
        *[!a-z0-9_-]*|'') die 2 "FUZZ_SLUG '${SLUG}' is not a safe slug" ;;
    esac
    if ! printf '%s' "${WHEEL_SHA256}" | grep -qE '^[0-9a-f]{64}$'; then
        die 2 "FUZZ_WHEEL_SHA256 is not 64 hex chars"
    fi

    log "=== fuzz ${SLUG} === runs=${RUNS} per-gen-timeout=${TIMEOUT_S}s yamls=${YAMLS} threads=${THREADS} wall=${WALL_SECONDS}s"

    # --- (a) Copy the bind-mounted wheel to /work (writable) and RE-VERIFY its
    # sha256. The bot already verified before mounting; this is defense in depth.
    # Mismatch -> fail fast with scan.sha256="mismatch".
    # Preserve the real basename when staging to /work so `uv pip install` can
    # parse the PEP 427 filename (it rejects a non-conformant name outright).
    local wheel="${WORK}/$(basename "${WHEEL_IN}")"
    log "staging mounted wheel ${WHEEL_IN}"
    cp "${WHEEL_IN}" "${wheel}"
    local actual
    actual="$(sha256sum "${wheel}" | awk '{print $1}')"
    if [ "${actual}" != "${WHEEL_SHA256}" ]; then
        log "sha256 mismatch: expected ${WHEEL_SHA256}, got ${actual}"
        # Bespoke result for the mismatch case so the bot can show scan.sha256.
        RESULT_WRITTEN=1
        STATUS="fail"; EXIT_CODE=3
        jq -n --arg slug "${SLUG}" --argjson lt "$(log_tail_json)" \
            '{slug:$slug, status:"fail", stats:{success:0,failure:0,timeout:0,ignored:0,total:0},
              scan:{sha256:"mismatch"}, exit_code:3, log_tail:$lt}' \
            > "${OUT}/result.json" 2>>"${LOG}" \
          || printf '{"slug":"%s","status":"fail","scan":{"sha256":"mismatch"},"exit_code":3,"log_tail":""}\n' \
                "${SLUG}" > "${OUT}/result.json"
        exit 3
    fi
    log "sha256 ok: ${actual}"

    # --- (b) Extract the wheel (a zip) to /work/extracted using Python's stdlib so
    # we never need an unzip binary; path-traversal is guarded.
    rm -rf "${EXTRACTED}"; mkdir -p "${EXTRACTED}"
    if ! python - "$wheel" "$EXTRACTED" <<'PY' 2>>"${LOG}"; then
import shutil, sys, zipfile
from pathlib import Path
src, dest = sys.argv[1], Path(sys.argv[2]).resolve()
with zipfile.ZipFile(src) as z:
    for m in z.infolist():
        target = (dest / m.filename).resolve()
        # Reject any member that would escape dest (zip-slip), same guard as
        # karen_review._download_and_expand_wheel. Extract each validated member
        # individually so what we check is exactly what we write.
        if not target.is_relative_to(dest):
            raise SystemExit(f"unsafe path in wheel: {m.filename}")
        if m.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with z.open(m) as s, open(target, "wb") as o:
            shutil.copyfileobj(s, o)
PY
        die 4 "wheel extraction failed"
    fi
    log "extracted wheel to ${EXTRACTED}"

    # --- (c) Wheel-targeted SCAN via the PINNED karen_review.py against the already
    # -extracted dir (--world-dir). karen_review requires the --changed manifest to
    # EXIST on disk, but with --world-dir + only deep checks selected its CONTENTS
    # are never read (schema/manifest checks aren't in the set) — so a placeholder
    # is sufficient and correct.
    local manifest_dir="${WORK}/worlds"
    local manifest="${manifest_dir}/${SLUG}.json"
    mkdir -p "${manifest_dir}"
    printf '{}' > "${manifest}"

    # pip_audit is intentionally NOT run here: it queries PyPI's advisory DB online
    # and this container is --network none. World wheels declare no deps, so the
    # audit surface is ~empty anyway; run it bot-side (trusted) later if desired.
    log "scanning extracted wheel (size/rom/network/bandit)"
    # Non-fatal: a scan that errors must NOT abort the fuzz; its findings are
    # advisory and surfaced in scan.json / result.json.scan.
    set +e
    python "${HARNESS_DIR}/karen_review.py" \
        --changed "${manifest}" \
        --world-dir "${EXTRACTED}" \
        --size-cap-mb "${SIZE_CAP_MB}" \
        --check size_sanity \
        --check no_rom_files \
        --check no_network_at_import \
        --check bandit \
        --output-summary "${OUT}/scan.json" >>"${LOG}" 2>&1
    local scan_rc=$?
    set -e
    log "karen_review exit=${scan_rc}"
    [ -s "${OUT}/scan.json" ] || log "warning: scan.json not written by karen_review"

    # ruff: purely advisory lint of the extracted source. Never fatal; capture JSON.
    set +e
    ruff check --output-format json "${EXTRACTED}" > "${OUT}/ruff.json" 2>>"${LOG}"
    local ruff_rc=$?
    set -e
    log "ruff exit=${ruff_rc}"

    # --- (d) Stage the BAKED core (incl. its relocatable .venv) into /work so it is
    # writable. No clone, no network — core is pinned into the image at build time.
    log "staging baked core ${BAKED_CORE} -> ${CORE}"
    rm -rf "${CORE}"
    cp -a "${BAKED_CORE}" "${CORE}"

    # If the operator bind-mounted a host.yaml (RO at ${HARNESS_DIR}/host.yaml),
    # install it where MWGG's get_settings() looks. With cwd == local_path == ${CORE}
    # and ${CORE} writable, user_path("host.yaml") resolves to ${CORE}/host.yaml.
    # Its <world>_options.rom_file entries should point at the read-only /roms mount
    # so ROM-dependent worlds (e.g. metroidfusion) can actually generate. Without
    # it, get_settings() falls back to a romless default and those worlds no-op.
    if [ -s "${HARNESS_DIR}/host.yaml" ]; then
        cp "${HARNESS_DIR}/host.yaml" "${CORE}/host.yaml"
        log "installed mounted host.yaml -> ${CORE}/host.yaml"
        if [ -d /roms ]; then
            log "roms mount present: $(find /roms -maxdepth 1 -type f 2>/dev/null | wc -l) file(s)"
        else
            log "warning: host.yaml mounted but /roms is absent"
        fi
    else
        log "no host.yaml mounted; ROM-dependent worlds will no-op (no base ROM)"
    fi

    log "installing candidate wheel into the baked venv (offline, --no-deps)"
    set +e
    (
        set -e
        cd "${CORE}"
        # shellcheck disable=SC1091
        . .venv/bin/activate
        # Core requirements are already baked into .venv; world wheels declare no
        # deps, so --no-deps + --offline guarantees zero network here.
        uv pip install --offline --no-deps "${wheel}"
    ) >>"${LOG}" 2>&1
    local setup_rc=$?
    set -e
    [ "${setup_rc}" -eq 0 ] || die 6 "offline wheel install into baked venv failed"

    # --- (e) Fetch the upstream fuzzer and sed-inject the PINNED bootstrap BEFORE
    # the `from worlds import` line (same anchor as fuzz_worlds.sh — never a line
    # number, fuzz.py is a moving target). Then run it under a hard wall.
    cd "${CORE}"
    log "using baked fuzz.py (${BAKED_FUZZER})"
    cp "${BAKED_FUZZER}" fuzz.py
    local worlds_line
    worlds_line="$(grep -n '^from worlds import' fuzz.py | head -n1 | cut -d: -f1)"
    [ -n "${worlds_line}" ] || die 7 "could not find 'from worlds import' anchor in fuzz.py"
    # `sed Nr file` inserts AFTER line N, so use (worlds_line - 1) to land the
    # bootstrap immediately BEFORE the worlds import.
    sed -i "$((worlds_line - 1))r ${HARNESS_DIR}/fuzz_bootstrap.py" fuzz.py
    log "injected fuzz_bootstrap.py before fuzz.py:${worlds_line}"

    # The fuzzer hand-builds argv for spawned workers (sys.argv=['-c',...]); the
    # bootstrap falls back to APFUZZ_GAMES, so export it for the single slug.
    export APFUZZ_GAMES="${SLUG}"

    # Run the fuzzer. Wall it with `timeout` (KILL after a grace TERM) so a hung
    # generation can't pin the container until the bot's outer wall fires. The
    # fuzzer's own non-zero exit is NOT fatal here — we classify from report.json.
    log "running fuzz.py (wall ${WALL_SECONDS}s)"
    set +e
    . .venv/bin/activate
    timeout --kill-after=30s "${WALL_SECONDS}" \
        python fuzz.py -r "${RUNS}" -t "${TIMEOUT_S}" -g "${SLUG}" -j "${THREADS}" -n "${YAMLS}" \
        >>"${LOG}" 2>&1
    local fuzz_rc=$?
    set -e
    log "fuzz.py exit=${fuzz_rc}"

    # --- (f) Classify report.json (written relative to fuzz.py's cwd = ${CORE}).
    local report="${CORE}/fuzz_output/report.json"
    if [ ! -f "${report}" ]; then
        # No report = fuzz.py crashed or was wall-killed. Hard fail with the rc.
        STATUS="fail"
        if [ "${fuzz_rc}" -eq 124 ] || [ "${fuzz_rc}" -eq 137 ]; then
            EXIT_CODE="${fuzz_rc}"
            die "${fuzz_rc}" "fuzz.py hit the ${WALL_SECONDS}s wall with no report.json"
        fi
        die 8 "no report.json (fuzz.py exit=${fuzz_rc})"
    fi
    # Preserve the raw report for debugging via the /out mount.
    cp -f "${report}" "${OUT}/report.json" 2>>"${LOG}" || true

    local classified
    classified="$(jq -r "${CLASSIFY_JQ}" "${report}" 2>>"${LOG}" || true)"
    if [ -z "${classified}" ]; then
        die 9 "report.json present but unparseable"
    fi
    local s_status s_succ s_fail s_to s_ign s_rom s_real s_total
    read -r s_status s_succ s_fail s_to s_ign s_rom s_real s_total <<< "${classified}"
    log "classified: status=${s_status} success=${s_succ} failure=${s_fail} timeout=${s_to} ignored=${s_ign} rom=${s_rom} real=${s_real} total=${s_total}"

    # --- (g) Assemble the verdict the trap will write. A pass/warn is a SUCCESSFUL
    # run (exit 0); only setup/verification failures are non-zero. A classifier
    # "fail" is a real world failure but still a completed run -> exit 0 with
    # status:"fail" (the bot reads status, and forces fail itself only on a
    # non-zero exit_code, so we keep exit 0 here to mean "the harness worked").
    STATUS="${s_status}"
    STATS_JSON="$(jq -n \
        --argjson success "${s_succ:-0}" \
        --argjson failure "${s_fail:-0}" \
        --argjson timeout "${s_to:-0}" \
        --argjson ignored "${s_ign:-0}" \
        --argjson total   "${s_total:-0}" \
        '{success:$success, failure:$failure, timeout:$timeout, ignored:$ignored, total:$total}')"
    EXIT_CODE=0
    write_result
    log "wrote /out/result.json (status=${STATUS})"
}

run
# The EXIT trap (on_exit) performs the final exit with EXIT_CODE; if run() reached
# write_result, RESULT_WRITTEN=1 means the trap won't clobber the rich result.
