#!/usr/bin/env bash
# Vendor a pyrofling snapshot (with the Granite submodule tree) into
# an rpmbuild-ready source tarball. Usage: make-pyrofling-tarball.sh [YYYYMMDD]
#
# The FFmpeg submodule is NOT vendored: on Linux, Granite links
# system FFmpeg (ffmpeg-free) via pkg-config; the submodule is only
# used for Windows/Android builds. Skipping it makes the clone much
# smaller and faster.
set -euo pipefail

VER="${1:-$(date -u +%Y%m%d)}"
SOURCES="$HOME/rpmbuild/SOURCES"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --recurse-submodules --shallow-submodules \
    --config submodule."ffmpeg".update=none \
    https://github.com/Themaister/pyrofling "$TMP/pyrofling-$VER"
git -C "$TMP/pyrofling-$VER" submodule status

mkdir -p "$SOURCES"
tar -C "$TMP" -cJf "$SOURCES/pyrofling-$VER.tar.xz" "pyrofling-$VER"
(cd "$SOURCES" && sha256sum "pyrofling-$VER.tar.xz")
echo "Done. Put '$VER' into the pyrofling.spec Version field."