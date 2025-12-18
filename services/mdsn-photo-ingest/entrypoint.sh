#!/usr/bin/env sh
set -e

MODE="${INGEST_MODE:-simulate}"

if [ "$MODE" = "simulate" ]; then
  echo "[entrypoint] Starting simulator mode (watching ${DEV_INBOX:-/app/dev_inbox})"
  exec python simulate.py
fi

echo "[entrypoint] Starting gunicorn for Flask app (mode=$MODE)"
exec gunicorn -b 0.0.0.0:${MDSN_PORT:-5055} --workers 1 --threads 2 app.main:app
