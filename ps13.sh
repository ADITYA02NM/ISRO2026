#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  PS13 — 3-Terminal Orchestrator
#
#  Option A (auto):  Creates tmux with 3 panes (recommended)
#  Option B (manual): Run 3 separate scripts in 3 terminals:
#                     Terminal 1 → ./ps13-ollama.sh
#                     Terminal 2 → ./ps13-fastapi.sh
#                     Terminal 3 → ./ps13-frontend.sh
#
#  Usage: bash ps13.sh
# ═══════════════════════════════════════════════════════════════

set -e

NOC_DIR="/home/ego/Documents/ISRO2026/NOC-Frontend"
LOG_DIR="/tmp/ps13"
mkdir -p "$LOG_DIR"

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║     🟢 PS13 — NOC Grid Boot Sequence            ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "  Checking for tmux..."

if command -v tmux &>/dev/null; then
  echo "  ✅ tmux found — launching 3-pane session"
  echo ""

  # Kill stale ports first
  for port in 3000 8000 11434; do
    fuser -k "${port}/tcp" 2>/dev/null || true
  done
  sleep 0.5

  SESSION="ps13"

  # Kill existing session if any
  tmux kill-session -t "$SESSION" 2>/dev/null || true
  sleep 0.3

  # Create session with first pane (Ollama)
  tmux new-session -d -s "$SESSION" -n "ps13" "bash -c '
    echo \"╔══════════════════════════════════════════════════╗\"
    echo \"║  [1/3] Starting Ollama (qwen3:8b)               ║\"
    echo \"╚══════════════════════════════════════════════════╝\"
    fuser -k 11434/tcp 2>/dev/null || true
    sleep 0.5
    ollama serve
  '"

  # Split vertically for FastAPI (right pane)
  tmux split-window -h -t "$SESSION:0" "bash -c '
    echo \"╔══════════════════════════════════════════════════╗\"
    echo \"║  [2/3] Starting FastAPI / RAG (noc_copilot.py)   ║\"
    echo \"╚══════════════════════════════════════════════════╝\"
    fuser -k 8000/tcp 2>/dev/null || true
    sleep 0.5
    echo \"Waiting for Ollama...\"
    for i in \$(seq 1 30); do
      if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo \"  ✅ Ollama ready\"
        break
      fi
      sleep 1
    done
    cd \"$NOC_DIR\"
    python3 noc_copilot.py
  '"

  # Split the right pane vertically for Frontend (bottom-right)
  tmux split-window -v -t "$SESSION:0" "bash -c '
    echo \"╔══════════════════════════════════════════════════╗\"
    echo \"║  [3/3] Building frontend & starting Express     ║\"
    echo \"╚══════════════════════════════════════════════════╝\"
    fuser -k 3000/tcp 2>/dev/null || true
    sleep 0.5
    echo \"Waiting for FastAPI...\"
    for i in \$(seq 1 30); do
      if curl -s http://localhost:8000/health >/dev/null 2>&1; then
        echo \"  ✅ FastAPI ready\"
        break
      fi
      sleep 1
    done
    cd \"$NOC_DIR\"
    echo \"Building frontend...\"
    npx vite build 2>&1 | tail -5
    echo \"✅ Build complete\"
    echo \"Starting Express on http://localhost:3000\"
    npx tsx server.ts
  '"

  # Set equal layout
  tmux select-layout -t "$SESSION:0" main-vertical 2>/dev/null || true

  # Sync panes so Ctrl+C kills all
  tmux set-option -t "$SESSION" synchronize-panes off

  echo ""
  echo "╔══════════════════════════════════════════════════╗"
  echo "║  ✅ tmux session \"ps13\" created                  ║"
  echo "║                                                ║"
  echo "║  Layout:                                        ║"
  echo "║  ┌────────────────────┬────────────────────┐    ║"
  echo "║  │  Terminal 1        │  Terminal 2        │    ║"
  echo "║  │  Ollama :11434     │  FastAPI :8000     │    ║"
  echo "║  │                    ├────────────────────┤    ║"
  echo "║  │                    │  Terminal 3        │    ║"
  echo "║  │                    │  Express :3000     │    ║"
  echo "║  └────────────────────┴────────────────────┘    ║"
  echo "║                                                ║"
  echo "║  Commands:                                      ║"
  echo "║    tmux attach -t ps13  → Enter session         ║"
  echo "║    Ctrl+B then arrows  → Navigate panes         ║"
  echo "║    Ctrl+C in a pane    → Stop that service      ║"
  echo "║    Ctrl+B then &       → Kill entire session    ║"
  echo "╚══════════════════════════════════════════════════╝"

  # Auto-attach
  tmux attach -t "$SESSION"
else
  echo "  ⚠️  tmux not found."
  echo ""
  echo "╔══════════════════════════════════════════════════╗"
  echo "║  Option 1: Install tmux                         ║"
  echo "║    sudo apt install tmux -y && bash ps13.sh     ║"
  echo "║                                                ║"
  echo "║  Option 2: Run 3 terminals manually:            ║"
  echo "║                                                ║"
  echo "║    Terminal 1:  bash ps13-ollama.sh             ║"
  echo "║    Terminal 2:  bash ps13-fastapi.sh            ║"
  echo "║    Terminal 3:  bash ps13-frontend.sh           ║"
  echo "╚══════════════════════════════════════════════════╝"
  echo ""
  echo "  Or install tmux with:"
  echo "    sudo apt install tmux -y"
  echo "    bash ps13.sh"
fi
