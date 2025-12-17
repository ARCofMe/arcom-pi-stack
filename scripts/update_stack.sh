#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

echo "[update_stack] Pulling repo and submodules..."
git pull --rebase
git submodule update --init --recursive

echo "[update_stack] Rebuilding containers..."
docker compose -f deploy/docker-compose.yml build --pull

echo "[update_stack] Restarting stack..."
docker compose -f deploy/docker-compose.yml up -d

echo "[update_stack] Done."
