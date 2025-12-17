#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="${ROOT_DIR}/backups"
TIMESTAMP="$(date +"%Y%m%d-%H%M%S")"
ARCHIVE_PATH="${1:-${BACKUP_DIR}/stack-backup-${TIMESTAMP}.tar.gz}"

mkdir -p "${BACKUP_DIR}"

echo "[backup_stack] Writing archive to ${ARCHIVE_PATH}"
tar -czf "${ARCHIVE_PATH}" -C "${ROOT_DIR}" deploy/data deploy/env

echo "[backup_stack] Done."
