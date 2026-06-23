# ISRO2026 NOC Copilot — 3-Terminal Startup Guide

## Overview

This guide walks you through starting the complete ISRO2026 air-gapped NOC Copilot system across 3 terminals. The system includes:
- **Ollama LLM** (qwen3:8b) + embeddings (nomic-embed-text)
- **FastAPI backend** with RAG pipeline and 7 trained ML models
- **Containerlab network topology** (PS13 lab simulation)
- **3D interactive dashboard** (browser-based)

**Total startup time**: ~2-3 minutes (after first-time model downloads)

---

## Prerequisites

### System Requirements
- Linux (Ubuntu 20.04+)
- 8GB+ RAM (16GB recommended)
- 20GB+ free disk space
- Docker + Containerlab installed
- Python 3.10+
- Ollama installed and running

### Verify Prerequisites
```bash
cd /home/ego/Documents/ISRO2026

# Check Python
python3 --version  # Should be 3.10+

# Check Docker
docker --version

# Check Containerlab
containerlab version

# Check Ollama
ollama --version

# Check venv
ls -la ml/venv/bin/python
```

If any prerequisite is missing, install it before proceeding.

---

## Terminal 1: Start Ollama LLM Server

**Purpose**: Serve the qwen3:8b language model and nomic-embed-text embeddings.

```bash
# Terminal 1
cd /home/ego/Documents/ISRO2026

# Start Ollama server (listens on localhost:11434)
ollama serve

# Expected output:
# 2026/06/24 12:00:00 "Listening on 127.0.0.1:11434"
```

**Verification**:
```bash
# In a separate terminal (not T1), test connectivity:
curl http://localhost:11434/api/tags
# Should return JSON with available models
```

**Keep this terminal running** — it's the LLM backbone.

---

## Terminal 2: Start FastAPI Backend

**Purpose**: Run the NOC Copilot API with RAG pipeline, ML models, and LLM interface.

```bash
# Terminal 2
cd /home/ego/Documents/ISRO2026

# Activate venv
source ml/venv/bin/activate

# Start FastAPI server (listens on 0.0.0.0:8000)
python -m uvicorn ml.noc_copilot:app --host 0.0.0.0 --port 8000 --reload

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
```

**Verification**:
```bash
# In a separate terminal, test the API:
curl http://localhost:8000/health
# Should return: {"status": "ok"}

# Test RAG endpoint:
curl -X POST http://localhost:8000/rag \
  -H "Content-Type: application/json" \
  -d '{"query": "What is network latency?"}'
# Should return RAG results with LLM response
```

**Keep this terminal running** — it's the API backbone.

---

## Terminal 3: Deploy Containerlab Network Topology

**Purpose**: Spin up the PS13 network simulation (routers, switches, hosts).

```bash
# Terminal 3
cd /home/ego/Documents/ISRO2026

# Deploy the topology
sudo containerlab deploy -t topology.clab.yml -v

# Expected output:
# INFO[0000] Containerlab v0.x.x started
# INFO[0001] Deploying topology from topology.clab.yml
# INFO[0010] Deployed 'ps13' topology
# INFO[0010] Deployed nodes:
#   - ps13-r1 (linux)
#   - ps13-r2 (linux)
#   - ps13-s1 (linux)
#   - ps13-h1 (linux)
#   - ps13-h2 (linux)
#   - ps13-h3 (linux)
```

**Verification**:
```bash
# List deployed containers
sudo containerlab inspect -t topology.clab.yml

# Test connectivity (from T3 or separate terminal)
sudo docker exec ps13-h1 ping -c 2 ps13-h2
# Should show successful pings
```

**Keep this terminal running** — it maintains the network topology.

---

## Browser: Open Dashboard

**Purpose**: Visualize the network topology and NOC metrics in real-time.

```bash
# In any terminal (or directly):
xdg-open /home/ego/Documents/ISRO2026/ml/noc-dashboard.html

# Or manually open in browser:
# File → Open → /home/ego/Documents/ISRO2026/ml/noc-dashboard.html
```

**Expected**:
- 3D network topology visualization (routers, switches, hosts)
- Real-time metrics (latency, throughput, packet loss)
- LLM chat interface (bottom-right)
- RAG search results panel

---

## Full Startup Sequence (Step-by-Step)

### Step 1: Open 3 Terminals
```bash
# Terminal 1, 2, 3 — all in /home/ego/Documents/ISRO2026
cd /home/ego/Documents/ISRO2026
```

### Step 2: Terminal 1 — Ollama
```bash
# T1
ollama serve
# Wait for: "Listening on 127.0.0.1:11434"
```

### Step 3: Terminal 2 — FastAPI
```bash
# T2
source ml/venv/bin/activate
python -m uvicorn ml.noc_copilot:app --host 0.0.0.0 --port 8000 --reload
# Wait for: "Application startup complete"
```

### Step 4: Terminal 3 — Containerlab
```bash
# T3
sudo containerlab deploy -t topology.clab.yml -v
# Wait for: "Deployed 'ps13' topology"
```

### Step 5: Browser — Dashboard
```bash
# Any terminal or directly:
xdg-open ml/noc-dashboard.html
# Dashboard should load with live topology and metrics
```

### Step 6: Verify All Systems
```bash
# In a 4th terminal, run validation:
python airgap_validate.py
# Should show 42/42 checks passing (or close to it)
```

---

## Testing the System

### Test 1: LLM Inference
```bash
curl -X POST http://localhost:8000/llm \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain network latency in 2 sentences"}'
```

### Test 2: RAG Pipeline
```bash
curl -X POST http://localhost:8000/rag \
  -H "Content-Type: application/json" \
  -d '{"query": "What causes packet loss?"}'
```

### Test 3: ML Model Predictions
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"model": "anomaly_detector", "data": [1.2, 0.8, 1.5, 0.9]}'
```

### Test 4: Network Connectivity
```bash
sudo docker exec ps13-h1 ping -c 2 ps13-h2
sudo docker exec ps13-r1 traceroute ps13-h3
```

---

## Troubleshooting

### Issue: Ollama fails to start
**Solution**:
```bash
# Check if Ollama is already running
ps aux | grep ollama

# Kill existing process
pkill -f "ollama serve"

# Restart
ollama serve
```

### Issue: FastAPI port 8000 already in use
**Solution**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Restart FastAPI on different port
python -m uvicorn ml.noc_copilot:app --host 0.0.0.0 --port 8001
```

### Issue: Containerlab deployment fails
**Solution**:
```bash
# Check Docker daemon
sudo systemctl status docker

# Clean up old containers
sudo containerlab destroy -t topology.clab.yml

# Redeploy
sudo containerlab deploy -t topology.clab.yml -v
```

### Issue: Dashboard doesn't load
**Solution**:
- Verify FastAPI is running: `curl http://localhost:8000/health`
- Check browser console for errors (F12)
- Verify file path: `/home/ego/Documents/ISRO2026/ml/noc-dashboard.html`
- Try hard refresh: `Ctrl+Shift+R`

### Issue: Models not loading
**Solution**:
```bash
# Check if models are downloaded
ollama list

# If missing, pull them
ollama pull qwen3:8b
ollama pull nomic-embed-text

# Restart FastAPI
# (Kill T2, restart with: python -m uvicorn ml.noc_copilot:app --host 0.0.0.0 --port 8000)
```

### Issue: airgap_validate.py shows failures
**Solution**:
```bash
# Run with verbose output
python airgap_validate.py -v

# Check specific service
curl http://localhost:8000/health
curl http://localhost:11434/api/tags

# Review logs in ml/logs/ (if available)
```

---

## Shutdown Sequence

### Graceful Shutdown
```bash
# Terminal 3: Stop Containerlab
sudo containerlab destroy -t topology.clab.yml

# Terminal 2: Stop FastAPI (Ctrl+C)
# Terminal 1: Stop Ollama (Ctrl+C)

# Verify cleanup
sudo docker ps  # Should be empty
ps aux | grep ollama  # Should be empty
```

---

## Performance Notes

- **First run**: Models download (~2-3 GB), takes 5-10 minutes
- **Subsequent runs**: ~2-3 minutes to full startup
- **Memory usage**: ~6-8 GB during operation
- **CPU**: 4+ cores recommended for smooth operation
- **Network**: Containerlab uses ~500 MB for topology

---

## Next Steps

1. **Run the system** using the 3-terminal sequence above
2. **Test each endpoint** (LLM, RAG, ML models)
3. **Interact with the dashboard** (query LLM, view metrics)
4. **Run validation**: `python airgap_validate.py`
5. **Review logs** in `ml/logs/` for any issues

---

## Support

For issues or questions:
- Check `Docs/` for architecture details
- Review `ml/noc_copilot.py` for API endpoints
- Check `airgap_validate.py` for system health
- Review containerlab logs: `sudo containerlab inspect -t topology.clab.yml`

---

**Last Updated**: 2026-06-24  
**Status**: Ready for deployment
