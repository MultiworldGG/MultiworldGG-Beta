# Hardened, self-contained image that fuzzes ONE untrusted MultiworldGG world.
#
# The bot (src/fuzz/runner.ts) runs this with:
#   --user 65532:65532 --read-only --cap-drop ALL --security-opt no-new-privileges
#   --tmpfs /tmp:rw,noexec,nosuid,size=512m  --tmpfs /work:rw,nosuid,size=4g
#   -v <host>/out:/out:rw
# and feeds every job input as an env var (FUZZ_*, MWGG_CORE_*, FUZZER_*).
#
# Because the root FS is read-only at runtime and /tmp is noexec, EVERYTHING the
# run needs must already be in the image, and every runtime write must land on
# /work or /out (both tmpfs/bind, both writable, neither noexec). The harness
# (fuzz_bootstrap.py + karen_review.py) is PINNED into the image — never fetched
# from a mutable branch at runtime — so a moving upstream can't change what runs.

FROM python:3.13-slim

# --- OS packages: the run script shells out to git/curl/jq; ca-certificates so
# TLS to github works. No build toolchain — wheels are prebuilt, and worlds are
# installed as wheels, not compiled.
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        git \
        curl \
        jq \
        ca-certificates; \
    rm -rf /var/lib/apt/lists/*

# --- Python tooling baked into the system site-packages so it resolves even when
# the world's own venv (created at runtime under /work) is active: the run script
# invokes these via absolute interpreter / PATH, not from the venv. Pinned-ish via
# a constraints-free install but recorded so `pip-audit` of the IMAGE is possible.
RUN set -eux; \
    pip install --no-cache-dir --upgrade pip; \
    pip install --no-cache-dir \
        uv \
        bandit \
        pip-audit \
        ruff \
        jsonschema

# --- Non-root identity. uid/gid 65532 matches the runner's `--user 65532:65532`
# (the conventional "nonroot" id). HOME is a real, world-writable dir so tools
# that insist on $HOME don't explode; but at RUNTIME the FS is read-only, so we
# also redirect every cache to /work via env below.
RUN set -eux; \
    groupadd --gid 65532 nonroot; \
    useradd --uid 65532 --gid 65532 --home-dir /home/nonroot --create-home --shell /usr/sbin/nologin nonroot

# Caches/config must never try to write the read-only root FS at runtime. /work
# is a writable tmpfs the bot always provides; point HOME and every XDG/tool cache
# there. (These dirs are created by the run script after /work is mounted.)
ENV HOME=/work \
    XDG_CACHE_HOME=/work/.cache \
    XDG_CONFIG_HOME=/work/.config \
    XDG_DATA_HOME=/work/.local/share \
    UV_CACHE_DIR=/work/.cache/uv \
    PIP_CACHE_DIR=/work/.cache/pip \
    PIP_NO_INPUT=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    GIT_TERMINAL_PROMPT=0 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    KIVY_NO_ARGS=1 \
    SKIP_ALL_INSTALLS=1 \
    MALLOC_ARENA_MAX=2

# --- PIN the harness into the image. These two files are vendored alongside this
# Dockerfile (copied from the Index repo's scripts/ at build time). Never curl
# them at runtime: the whole point is a reproducible, audited harness.
WORKDIR /opt/fuzz
COPY karen_review.py /opt/fuzz/karen_review.py
COPY fuzz_bootstrap.py /opt/fuzz/fuzz_bootstrap.py
COPY run_fuzz.sh /opt/fuzz/run_fuzz.sh
RUN chmod 0555 /opt/fuzz/run_fuzz.sh /opt/fuzz/karen_review.py /opt/fuzz/fuzz_bootstrap.py

# Mount points for the OPTIONAL read-only ROM support (bot adds `-v …:/roms:ro`
# and `-v …:/opt/fuzz/host.yaml:ro` only when FUZZ_ROM_DIR / FUZZ_HOST_YAML are
# set). The host.yaml needs a pre-existing target file because the runtime root
# FS is read-only; an empty placeholder also means "no host.yaml" when unmounted
# (the run script checks for a NON-empty file), preserving the romless default.
RUN set -eux; \
    mkdir -p /roms; chmod 0555 /roms; \
    : > /opt/fuzz/host.yaml; chmod 0444 /opt/fuzz/host.yaml

# Drop to the unprivileged user for the default run. The bot pins this again with
# --user, so this is defense-in-depth / correct behavior for a bare `docker run`.
USER 65532:65532

ENTRYPOINT ["/opt/fuzz/run_fuzz.sh"]
