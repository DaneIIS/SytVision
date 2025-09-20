#!/usr/bin/env bash
set -euo pipefail

# --- Variables ---
REPO_URL="https://github.com/DaneIIS/SytVision.git"
REPO_DIR="SytVision"

# --- Clone repo if not already present ---
if [ ! -d "$REPO_DIR" ]; then
  echo "[INFO] Cloning repository..."
  git clone "$REPO_URL"
else
  echo "[INFO] Repository already cloned, pulling latest..."
  git -C "$REPO_DIR" pull
fi

cd "$REPO_DIR"

# --- Ensure host directories exist for volumes ---
echo "[INFO] Creating host directories for volumes..."
mkdir -p ./nvr/{config,storage,segments,snapshots,thumbnails,event_clips}

# --- Build and start containers ---
echo "[INFO] Building images (no cache)..."
docker compose build --no-cache --progress=plain

echo "[INFO] Starting containers..."
docker compose up -d

# --- Verification ---
echo "[INFO] Current container status:"
docker compose ps

echo "[INFO] Checking frontend availability on http://localhost:8080 ..."
curl -I http://localhost:8080 || true

echo "[INFO] Checking backend API proxy on http://localhost:8080/api/ ..."
curl -Ssf http://localhost:8080/api/ || true
