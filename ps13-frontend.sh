#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  PS13 — Terminal 3: Frontend Build + Express Server
#  Run in third terminal tab/window (after FastAPI is ready)
# ═══════════════════════════════════════════════════════════════

NOC_DIR="/home/ego/Documents/ISRO2026/NOC-Frontend"

echo "╔══════════════════════════════════════════════════╗"
echo "║  [3/3] Building frontend & starting Express     ║"
echo "╚══════════════════════════════════════════════════╝"

# Kill stale on port 3000
fuser -k 3000/tcp 2>/dev/null || true
sleep 0.5

# Wait for FastAPI
echo "Waiting for FastAPI..."
for i in $(seq 1 30); do
  if curl -s http://localhost:8000/health >/dev/null 2>&1; then
    echo "  ✅ FastAPI ready"
    break
  fi
  sleep 1
done

cd "$NOC_DIR"

# Build frontend
echo "Building frontend..."
npx vite build 2>&1 | tail -5
echo "✅ Build complete"

# Start Express server
echo "Starting Express on http://localhost:3000"
npx tsx server.ts
