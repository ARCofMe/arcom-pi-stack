#!/usr/bin/env bash
set -euo pipefail

echo "[bootstrap_pi] Installing Docker Engine..."
curl -fsSL https://get.docker.com | sh

echo "[bootstrap_pi] Enabling Docker service..."
sudo systemctl enable docker
sudo systemctl start docker

echo "[bootstrap_pi] Installing docker-compose plugin..."
sudo apt-get update
sudo apt-get install -y docker-compose-plugin

echo "[bootstrap_pi] Adding current user to docker group (log out/in after this)..."
sudo usermod -aG docker "$USER"

echo "[bootstrap_pi] Done. Reboot recommended."
