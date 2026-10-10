# hadolint global ignore=SC1090,SC1091

# One image per webhost role: `docker build --target web|hoster|generator|upgrader`.

# Source
FROM scratch AS release
WORKDIR /release
ADD https://github.com/Ijwu/Enemizer/releases/latest/download/ubuntu.16.04-x64.zip Enemizer.zip

# Enemizer
FROM alpine:3.21 AS enemizer
ARG TARGETARCH
WORKDIR /release
COPY --from=release /release/Enemizer.zip .

# No release for arm architecture. Skip.
RUN if [ "$TARGETARCH" = "amd64" ]; then \
    apk add unzip=6.0-r15 --no-cache && \
    unzip -u Enemizer.zip -d EnemizerCLI && \
    chmod -R 777 EnemizerCLI; \
    else mkdir EnemizerCLI; fi

# Cython builder stage
FROM python:3.13 AS cython-builder

WORKDIR /build

# Copy and install requirements first (better caching)
COPY requirements.txt WebHostLib/requirements.txt

RUN pip install --no-cache-dir -r \
    WebHostLib/requirements.txt \
    "setuptools>=75,<81"

COPY _speedups.pyx .
COPY intset.h .

RUN cythonize -b -i _speedups.pyx

# Every image runs this interpreter: the worlds venv the upgrader creates links to
# it, and the other images execute that link when they import ModuleUpdate.
FROM python:3.13-slim-trixie AS runtime
ENV PYTHONUNBUFFERED=1
# Opt this image into the mwgg_venv worlds-venv pathway in ModuleUpdate.
ENV MWGG_USE_WORLDS_VENV=1
RUN mkdir -p /root/.local/share/MultiworldGG
WORKDIR /app

# Sole writer of the worlds venv; needs none of the webhost code or its requirements.
FROM runtime AS upgrader
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir uv packaging PyYAML
COPY application.yaml BaseUtils.py ModuleUpdate.py ./
COPY tools/mwgg_upgrade.py tools/
RUN mkdir -p custom_worlds
ENTRYPOINT ["python", "tools/mwgg_upgrade.py"]

# Compilers stay in this stage; the app images copy only the finished venv.
FROM runtime AS deps
ENV VIRTUAL_ENV=/opt/venv
ENV PATH=$VIRTUAL_ENV/bin:$PATH
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc=4:14.2.0-1 \
    libc6-dev \
    g++=4:14.2.0-1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN python -m venv $VIRTUAL_ENV
# uv is required at runtime by ModuleUpdate.find_uv() (called at import time)
RUN pip install --no-cache-dir uv
# Root requirements.txt: base + world-runtime deps (pathspec, PyYAML, xxtea,
# aiohttp, etc.) - imported at module load or needed by world generation.
COPY requirements.txt requirements.txt
COPY WebHostLib/requirements-worker.txt WebHostLib/requirements-worker.txt
RUN pip install --no-cache-dir \
    -r requirements.txt \
    -r WebHostLib/requirements-worker.txt

# The code tree every app image copies in last, so code changes never invalidate dependency layers.
FROM runtime AS app-tree
COPY . .
COPY --from=cython-builder /build/*.so ./
# /app/roms -> /roms lets a host.yaml use roms/<file> entries, the convention the fuzz image shares.
RUN rm -f _speedups.pyx _speedups.pyxbld intset.h && \
    mkdir -p custom_worlds && \
    ln -s /roms roms

FROM runtime AS app
ENV VIRTUAL_ENV=/opt/venv
ENV PATH=$VIRTUAL_ENV/bin:$PATH
# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends libtk8.6=8.6.16-1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
COPY --from=deps /opt/venv /opt/venv
# Runtime data lives outside /app so nothing is ever mounted over the code
# tree; deploy/docker-compose.yml mounts these paths.
ENV MWGG_DB_FILE=/db/ap.db3 \
    MWGG_UPLOAD_FOLDER=/uploads \
    MWGG_LOGS_FOLDER=/logs \
    MWGG_GENERATED_FOLDER=/static/generated
RUN mkdir -p /db /uploads /logs /static/generated /roms
# Ensure no runtime ModuleUpdate.
ENV SKIP_REQUIREMENTS_UPDATE=true

FROM app AS web
# Outside /app, so the code layer below stays identical to the hoster's and generator's.
COPY WebHostLib/requirements-worker.txt WebHostLib/requirements.txt /tmp/webhost-requirements/
RUN pip install --no-cache-dir \
    -r /tmp/webhost-requirements/requirements.txt \
    gunicorn==23.0.0
COPY --from=app-tree /app /app
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD ["python", "-c", "import os, urllib.request; urllib.request.urlopen(f\"http://127.0.0.1:{os.environ.get('PORT', '8000')}/api/datapackage_checksum\", timeout=5)"]
ENTRYPOINT ["gunicorn", "-c", "gunicorn.conf.py"]

FROM app AS hoster
COPY --from=app-tree /app /app
ENTRYPOINT ["python", "WebHost.py", "--role", "hoster"]

FROM app AS generator
COPY --from=enemizer /release/EnemizerCLI /app/EnemizerCLI
COPY --from=app-tree /app /app
ENTRYPOINT ["python", "WebHost.py", "--role", "generator"]
