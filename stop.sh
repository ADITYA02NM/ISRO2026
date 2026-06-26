#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
# stop.sh — PS13 Project Shutdown
# =================================================================
# Kills all services in order:
#   1. Express (NOC Frontend, port 3000)
#   2. FastAPI (RAG + ML, port 8000)
#   3. Ollama  (LLM, port 11434)
# =================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}═══════════════════════════════════════════════${NC}"
echo -e "${CYAN}  PS13 — Shutting Down All Services${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════${NC}"
echo ""

# ── 1. Express (NOC Frontend on :3000) ──────────────────────────
EXPRESS_PIDS=$(pgrep -f "tsx server" 2>/dev/null || true)
if [ -n "$EXPRESS_PIDS" ]; then
  echo -e "  ${RED}✕${NC} Stopping Express (port 3000)..."
  kill $EXPRESS_PIDS 2>/dev/null || true
  sleep 1
  if pgrep -f "tsx server" >/dev/null 2>&1; then
    kill -9 $EXPRESS_PIDS 2>/dev/null || true
  fi
  echo -e "  ${GREEN}✓${NC} Express stopped"
else
  echo -e "  ${GREEN}✓${NC} Express not running"
fi

# ── 2. FastAPI / Uvicorn (RAG + ML on :8000) ─────────────────────
FASTAPI_PIDS=$(pgrep -f "uvicorn noc_copilot" 2>/dev/null || true)
if [ -n "$FASTAPI_PIDS" ]; then
  echo -e "  ${RED}✕${NC} Stopping FastAPI (port 8000)..."
  kill $FASTAPI_PIDS 2>/dev/null || true
  sleep 1
  if pgrep -f "uvicorn noc_copilot" >/dev/null 2>&1; then
    kill -9 $FASTAPI_PIDS 2>/dev/null || true
  fi
  echo -e "  ${GREEN}✓${NC} FastAPI stopped"
else
  echo -e "  ${GREEN}✓${NC} FastAPI not running"
fi

# ── 3. Ollama (LLM on :11434) ────────────────────────────────────
OLLAMA_PIDS=$(pgrep -f "ollama" 2>/dev/null || true)
if [ -n "$OLLAMA_PIDS" ]; then
  echo -e "  ${RED}✕${NC} Stopping Ollama (port 11434)..."
  kill $OLLAMA_PIDS 2>/dev/null || true
  sleep 1
  if pgrep -f "ollama" >/dev/null 2>&1; then
    kill -9 $OLLAMA_PIDS 2>/dev/null || true
  fi
  echo -e "  ${GREEN}✓${NC} Ollama stopped"
else
  echo -e "  ${GREEN}✓${NC} Ollama not running"
fi

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
echo -e "${GREEN}  All services stopped.${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════${NC}"
