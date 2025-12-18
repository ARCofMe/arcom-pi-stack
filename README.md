## Overview
This repo holds the ARCoM Pi stack for Raspberry Pi 4, built to run via Docker Compose. It wires together:
- dispatcher-routing-app backend (Python)
- dispatcher-routing-app frontend (Node/Vite/React)
- mdsn-photo-ingest (Python/Flask) for ingesting photos, parsing SRIDs, and auditing to SQLite

Shared libraries live under `libs/` and are installed into Python services in editable mode when available.

## Services and Ports
- dispatcher-backend: `8000` (configurable via `DISPATCHER_BACKEND_PORT`)
- dispatcher-frontend: `4173` (configurable via `DISPATCHER_FRONTEND_PORT`)
- mdsn-photo-ingest: `5055` (configurable via `MDSN_PORT`)

Persistent data (including SQLite) is stored in `deploy/data`.

## Prerequisites
- Docker Engine + docker-compose plugin
- Git with access to private submodules (bluefolder-api, optimized-routing-extension, and the service repos listed below)

## Fetching Code
Clone and pull submodules:
```bash
git clone https://github.com/ARCofMe/arcom-pi-stack.git
cd arcom-pi-stack
git submodule update --init --recursive
```

The dispatcher and photo ingest services come from private repos. Once you have credentials, add them as submodules (or clone into the same paths):
```bash
git submodule add https://github.com/ARCofMe/dispatcher-routing-app.git services/dispatcher-routing-app/app
git submodule add https://github.com/ARCofMe/photo_ingest.git services/mdsn-photo-ingest/external
git submodule update --init --recursive
```

If the repos are private, use SSH URLs or configure a GitHub token.

## Environment
Copy and fill the env files (keep secrets out of git):
```bash
cp deploy/env/stack.env.example deploy/env/stack.env
cp deploy/env/dispatcher.env.example deploy/env/dispatcher.env
cp deploy/env/photo_ingest.env.example deploy/env/photo_ingest.env
```

Key variables:
- `DISPATCHER_BACKEND_CMD`, `DISPATCHER_FRONTEND_CMD`: how to start the dispatcher processes inside the containers.
- `INGEST_MODE`: `simulate` (default) watches `services/mdsn-photo-ingest/dev_inbox/<SRID>/` for images.
- `BLUEFOLDER_API_KEY`: required once real attachments are enabled.
- `BLUEFOLDER_ATTACHMENTS_BASE_URL`: use `https://api.bluefolder.com/api/2.0` for the global attachment endpoint (preferred) and set `BLUEFOLDER_BASE_URL` to your account host (e.g., `https://menhcomputers.bluefolder.com`).

## Running Locally
On x86/mac hosts, avoid qemu emulation by setting `DOCKER_DEFAULT_PLATFORM` to your native arch (e.g., `linux/amd64`) when building:
```bash
export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker compose -f deploy/docker-compose.yml build
docker compose -f deploy/docker-compose.yml up -d
```

For Pi builds, leave it as default (linux/arm64) or set accordingly:
```bash
export DOCKER_DEFAULT_PLATFORM=linux/arm64
docker compose -f deploy/docker-compose.yml build
docker compose -f deploy/docker-compose.yml up -d
```

After the stack is up:
- dispatcher-backend health: http://localhost:8000/health (falls back to `/` if not defined)
- dispatcher-frontend: http://localhost:4173 (binds `0.0.0.0`, accessible on LAN via Pi IP/hostname)
- mdsn-photo-ingest health: http://localhost:5055/health

If the frontend is bind-mounted for live code, node modules live in a named volume (`node_modules_frontend`). The entrypoint will run `npm install` if they are missing.

Photo ingest simulator: when `INGEST_MODE=simulate`, the container runs `python simulate.py` (from the photo_ingest repo) and watches `services/mdsn-photo-ingest/dev_inbox/<SRID>/` for images.

Logs:
```bash
docker compose -f deploy/docker-compose.yml logs -f mdsn-photo-ingest
```

## Data and Backups
- All persistent state lives in `deploy/data`.
- Use `scripts/backup_stack.sh` to archive `deploy/data` and `deploy/env`:
  ```bash
  ./scripts/backup_stack.sh
  ```

## Updating
Pull the latest code, submodules, rebuild, and restart:
```bash
./scripts/update_stack.sh
```

## Notes and TODOs
- BlueFolder attachments are stubbed until credentials are provided; the interface is in `services/mdsn-photo-ingest/app/bluefolder_client.py`.
- If the shared libs cannot be installed in editable mode, the Dockerfiles fall back to `PYTHONPATH` pointing at `/libs`.
- Ensure the dispatcher and photo ingest submodules are added before production deployment.
