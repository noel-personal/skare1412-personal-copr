#!/usr/bin/env bash
# Turn a local/private git checkout into a source tarball for rpmbuild.
# Usage: make-local-tarball.sh <repo-path> <name> <version>
# NOTE: git archive does NOT include submodules — if the repo has
# submodules, clone --recursive from the local path instead.
set -euo pipefail

REPO="$(realpath "${1:?usage: $0 <repo-path> <name> <version>}")"
NAME="${2:?missing name}"
VER="${3:?missing version}"
SOURCES="$HOME/rpmbuild/SOURCES"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir "$TMP/$NAME-$VER"
git -C "$REPO" archive --format=tar HEAD | tar -C "$TMP/$NAME-$VER" -xf -

mkdir -p "$SOURCES"
tar -C "$TMP" -cJf "$SOURCES/$NAME-$VER.tar.xz" "$NAME-$VER"
(cd "$SOURCES" && sha256sum "$NAME-$VER.tar.xz")