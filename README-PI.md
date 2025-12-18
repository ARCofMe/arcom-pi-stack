## Dec 22 Pi Day Runbook

Step-by-step to bring the stack up on a Raspberry Pi 4.

1) Flash OS and enable SSH
   - Use Raspberry Pi Imager to flash Raspberry Pi OS Lite (64-bit) to the SD card.
   - In Imager, enable SSH (prefer key-based), set hostname, and configure Wi-Fi or Ethernet.
   - Insert the card and boot the Pi.

2) Update system and install Docker + compose plugin
   ```bash
   sudo apt-get update && sudo apt-get upgrade -y
   curl -fsSL https://get.docker.com | sh
   sudo systemctl enable docker --now
   sudo apt-get install -y docker-compose-plugin
   sudo usermod -aG docker $USER  # log out/in afterwards
   ```
   (Alternatively run `./scripts/bootstrap_pi.sh` after cloning in step 4.)

3) Clone the stack with submodules
   ```bash
   git clone https://github.com/ARCofMe/arcom-pi-stack.git
   cd arcom-pi-stack
   git submodule update --init --recursive
   ```
   Add the service repos (private) once authenticated:
   ```bash
   git submodule add https://github.com/ARCofMe/dispatcher-routing-app.git services/dispatcher-routing-app/app
   git submodule add https://github.com/ARCofMe/photo_ingest.git services/mdsn-photo-ingest/external
   git submodule update --init --recursive
   ```
   Use SSH URLs or a GitHub token if HTTPS prompts for credentials.

4) Prepare environment files
   ```bash
   cp deploy/env/stack.env.example deploy/env/stack.env
   cp deploy/env/dispatcher.env.example deploy/env/dispatcher.env
   cp deploy/env/photo_ingest.env.example deploy/env/photo_ingest.env
   # edit values as needed (ports, commands, API keys)
   ```

5) Start the stack
   - On Pi: builds use arm64 by default.
     ```bash
     docker compose -f deploy/docker-compose.yml build
     docker compose -f deploy/docker-compose.yml up -d
     ```
   - On x86/mac test hosts, set the platform to avoid qemu emulation:
     ```bash
     export DOCKER_DEFAULT_PLATFORM=linux/amd64
     docker compose -f deploy/docker-compose.yml build
     docker compose -f deploy/docker-compose.yml up -d
     ```

6) Validate services
   - Backend health: `curl http://localhost:8000/health` (falls back to `/` if not defined).
   - Frontend: open `http://<pi-hostname>:4173` from any LAN device (frontend command binds `0.0.0.0`).
   - Photo ingest: `curl http://localhost:5055/health`.

7) Simulate photo ingest (optional)
   - With `INGEST_MODE=simulate`, drop images in `services/mdsn-photo-ingest/dev_inbox/<SRID>/`.
   - The container will run `python simulate.py` (from the photo_ingest repo) to process new files and log to SQLite under `deploy/data/mdsn_photo_ingest.db`.

8) Backups
   ```bash
   ./scripts/backup_stack.sh  # archives deploy/data and deploy/env
   ```
   Copy the archive off-box periodically.

9) Updating the stack
   ```bash
   ./scripts/update_stack.sh
   ```

## Logging and Rotation
- Containers log to stdout/stderr. Docker forwards to journald by default on Pi OS; manage size with:
  ```bash
  sudo journalctl --vacuum-time=7d
  ```
- For heavier traffic later, consider enabling Docker JSON log rotation via `/etc/docker/daemon.json`.

## Notes
- BlueFolder attachments are stubbed until credentials are available; interface lives in `services/mdsn-photo-ingest/app/bluefolder_client.py`.
- Shared libs under `/libs` are installed in editable mode; Dockerfiles fall back to `PYTHONPATH` if needed.
- Use `MDSN_SCAN_INTERVAL` to tune the dev inbox polling rate and reduce SD wear; tmpfs is mounted to `/tmp` for the ingest container.
