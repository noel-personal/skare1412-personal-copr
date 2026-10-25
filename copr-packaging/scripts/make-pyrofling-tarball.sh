#!/usr/bin/env bash
# Vendor a pyrofling snapshot (with Granite + FFmpeg submodules) into
# an rpmbuild-ready source tarball. Usage: make-pyrofling-tarball.sh [YYYYMMDD]
set -euo pipefail

VER="${1:-$(date -u +%Y%m%d)}"
SOURCES="$HOME/rpmbuild/SOURCES"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git clone --recursive https://github.com/Themaister/pyrofling "$TMP/pyrofling-$VER"

mkdir -p "$SOURCES"
tar -C "$TMP" -cJf "$SOURCES/pyrofling-$VER.tar.xz" "pyrofling-$VER"
(cd "$SOURCES" && sha256sum "pyrofling-$VER.tar.xz")
echo "Done. Put '$VER' into the pyrofling.spec Version field."