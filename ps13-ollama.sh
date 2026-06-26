#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  PS13 — Terminal 1: Ollama
#  Run in first terminal tab/window
# ═══════════════════════════════════════════════════════════════

echo "╔══════════════════════════════════════════════════╗"
echo "║  [1/3] Starting Ollama (qwen3:8b)               ║"
echo "╚══════════════════════════════════════════════════╝"

# Kill stale on port 11434
fuser -k 11434/tcp 2>/dev/null || true
sleep 0.5

ollama serve
