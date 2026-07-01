#!/bin/bash
set -euo pipefail

echo "[dev] Installing backend dependencies..."
pip install -r backend/requirements.txt
pip install pytest pytest-asyncio httpx ruff bandit

echo "[dev] Installing frontend deps..."
cd frontend
npm install
cd ..

echo "[dev] Setup complete."
echo "Next: make dev-backend + make dev-frontend"
