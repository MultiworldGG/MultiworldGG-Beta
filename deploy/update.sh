#!/usr/bin/env bash
# Rebuild the MWGG stack and RECLAIM the image layers the rebuild orphaned, so
# /var/lib/docker/overlay2 stays bounded.
#
# Why this exists: the fuzz and multiworld images are multi-GB. Every rebuild
# retags `:latest` and leaves the PREVIOUS image dangling (<none>:<none>) — those
# orphaned layers are what silently fill the disk. This couples the cleanup to the
# rebuild so the update is self-cleaning; run it instead of a bare
# `docker compose build && docker compose up -d`.
#
# Usage (run from anywhere):
#   deploy/update.sh            # build webhost + bot + fuzz, recreate, prune
#   deploy/update.sh fuzz       # only the fuzz image
#   deploy/update.sh bot        # only the github-bots image
#   deploy/update.sh webhost    # only the multiworld/web image
#   deploy/update.sh none       # no build; just recreate + prune (after a manual build)
#
# Env:
#   FUZZ_IMAGE       tag to build the fuzz image as; MUST match the bot's
#                    FUZZ_IMAGE (default mirrors docker-compose.yml).
#   FUZZ_BUILD_ARGS  extra `docker build` args for the fuzz image, e.g.
#                    "--build-arg MWGG_CORE_REF=somebranch" (defaults are baked in).
set -euo pipefail

cd "$(dirname "$0")"   # deploy/ — `docker compose` uses ./docker-compose.yml here

FUZZ_IMAGE="${FUZZ_IMAGE:-ghcr.io/multiworldgg/multiworldgg-fuzz:latest}"
target="${1:-all}"

build_bot()     { docker compose build github-bots; }
build_webhost() { docker compose build multiworld; }   # `web` reuses this image
build_fuzz() {
  # karen_review.py + fuzz_bootstrap.py are vendored in ../GitHubLib/fuzz-image;
  # re-copy them from the Index repo's scripts/ if the harness changed (see that
  # dir's README). Core + fuzz.py are fetched at build time via Dockerfile ARGs.
  # shellcheck disable=SC2086  # FUZZ_BUILD_ARGS is intentionally word-split
  docker build ${FUZZ_BUILD_ARGS:-} -t "$FUZZ_IMAGE" ../GitHubLib/fuzz-image
}

case "$target" in
  all)     build_webhost; build_bot; build_fuzz ;;
  bot)     build_bot ;;
  webhost) build_webhost ;;
  fuzz)    build_fuzz ;;
  none)    ;;
  *) echo "unknown target '$target' (all|bot|webhost|fuzz|none)" >&2; exit 2 ;;
esac

# Recreate with the freshly-built images; pull only images we DON'T build locally
# (nudenet/nginx/proxy), and only when absent.
docker compose up -d --pull missing

# Reclaim. The images we just replaced are now dangling, plus the build cache.
# Dangling-only and NO --volumes, so this never removes a tagged in-use image or a
# named volume (app_volume / github_bots_state). This is the whole point: overlay2
# stops growing one orphaned multi-GB image per rebuild.
docker image prune -f
docker builder prune -f

echo "update.sh: done — $(docker system df --format '{{.Type}} {{.Reclaimable}}' 2>/dev/null | tr '\n' ' ')"
