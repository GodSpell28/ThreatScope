#!/bin/bash
set -euo pipefail

echo "[validate] Checking docker compose config..."
docker compose config > /dev/null

echo "[validate] Building backend image..."
docker compose build backend

echo "[validate] Starting data services..."
docker compose up -d postgres elasticsearch redis

echo "[validate] Waiting for health..."
for service in postgres elasticsearch redis; do
  echo " - $service"
  docker compose ps --format "{{.Name}}	{{.Health}}" | grep -E "^${service}.*healthy$" || (
    echo "[error] $service not healthy"
    docker compose ps
    exit 1
  )
done

echo "[validate] Stack looks good."
