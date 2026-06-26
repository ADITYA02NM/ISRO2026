#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  PS13 — Terminal 2: FastAPI / RAG
#  Run in second terminal tab/window (after Ollama is ready)
# ═══════════════════════════════════════════════════════════════

NOC_DIR="/home/ego/Documents/ISRO2026/NOC-Frontend"

echo "╔══════════════════════════════════════════════════╗"
echo "║  [2/3] Starting FastAPI / RAG (noc_copilot.py)   ║"
echo "╚══════════════════════════════════════════════════╝"

# Kill stale on port 8000
fuser -k 8000/tcp 2>/dev/null || true
sleep 0.5

# Wait for Ollama
echo "Waiting for Ollama..."
for i in $(seq 1 30); do
  if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "  ✅ Ollama ready"
    break
  fi
  sleep 1
done

cd "$NOC_DIR"
python3 noc_copilot.py
