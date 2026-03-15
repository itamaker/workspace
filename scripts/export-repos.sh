#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST_DIR="${1:-${ROOT_DIR}/dist/repos}"
PROJECTS=(skillforge runlens ragcheck promptdeck datasetlint go-chrome-ai)

mkdir -p "${DEST_DIR}"

for project in "${PROJECTS[@]}"; do
  target="${DEST_DIR}/${project}"
  if [[ -e "${target}" ]]; then
    echo "target already exists: ${target}" >&2
    exit 1
  fi

  mkdir -p "${target}"
  tar -C "${ROOT_DIR}/${project}" \
    --exclude "./dist" \
    --exclude "./output" \
    --exclude "./${project}" \
    --exclude "./.git" \
    -cf - . | tar -C "${target}" -xf -
  printf 'exported %s -> %s\n' "${project}" "${target}"
done
