#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OWNER=""
VERSION=""
TAP_DIR="${ROOT_DIR}/homebrew-tap"
PROJECTS=(skillforge runlens ragcheck promptdeck datasetlint)
TMP_DIR=""

usage() {
  echo "Usage: $0 --owner <project-repo-owner> --version <v0.1.0> [--tap-dir <dir>]" >&2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --owner)
      OWNER="$2"
      shift 2
      ;;
    --version)
      VERSION="$2"
      shift 2
      ;;
    --tap-dir)
      TAP_DIR="$2"
      shift 2
      ;;
    *)
      usage
      exit 1
      ;;
  esac
done

if [[ -z "${OWNER}" || -z "${VERSION}" ]]; then
  usage
  exit 1
fi

mkdir -p "${TAP_DIR}/Formula"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

for project in "${PROJECTS[@]}"; do
  checksum_file="${ROOT_DIR}/${project}/dist/checksums.txt"
  if [[ ! -f "${checksum_file}" ]]; then
    project_tmp_dir="${TMP_DIR}/${project}"
    mkdir -p "${project_tmp_dir}"
    gh release download "${VERSION}" -R "${OWNER}/${project}" -p checksums.txt -D "${project_tmp_dir}" >/dev/null
    checksum_file="${project_tmp_dir}/checksums.txt"
  fi

  if [[ ! -f "${checksum_file}" ]]; then
    echo "missing checksum file for ${project}" >&2
    exit 1
  fi

  "${ROOT_DIR}/${project}/scripts/render-homebrew-formula.sh" \
    --owner "${OWNER}" \
    --repo "${project}" \
    --version "${VERSION}" \
    --checksums "${checksum_file}" \
    > "${TAP_DIR}/Formula/${project}.rb"

  printf 'rendered %s -> %s\n' "${project}" "${TAP_DIR}/Formula/${project}.rb"
done
