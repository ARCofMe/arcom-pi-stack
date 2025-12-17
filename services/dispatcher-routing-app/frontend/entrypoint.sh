#!/usr/bin/env sh
set -e

# Install dependencies if node_modules is missing or empty (common when bind-mounting host code).
if [ ! -d /app/node_modules ] || [ -z "$(ls -A /app/node_modules 2>/dev/null)" ]; then
  echo "[entrypoint] Installing frontend dependencies..."
  npm install
fi

exec "$@"
