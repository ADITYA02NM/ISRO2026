---
created: 2026-06-23
tags: [ps13, llm, ollama, qwen]
---

# LLM Interface — `ml/llm_interface.py`

**260 lines.** Ollama client wrapper for local LLM inference with a NOC-operator system prompt.

## Models

| Model | Size | Purpose | Pull Command |
|-------|------|---------|-------------|
| `qwen3:8b` | 5.2 GB | Primary LLM for diagnosis & chat | `ollama pull qwen3:8b` |
| `gemma3:12b` | 8.1 GB | Alternative (already cached) | `ollama pull gemma3:12b` |
| `nomic-embed-text` | 274 MB | Text embeddings for RAG | `ollama pull nomic-embed-text` |

## System Prompt

The LLM is prompted as a **senior NOC engineer** for a 4-site MPLS SD-WAN network spanning Bangalore, Mumbai, Chennai, and Delhi. Instructions include:
- Identify root cause vs symptom
- Isolate to specific site, device, circuit
- Rank severity and time-sensitivity
- Recommend concrete actions
- Use domain-specific language (TTI, BGP flaps, CRC errors)

## Methods

| Method | Input | Output |
|--------|-------|--------|
| `generate(prompt, system)` | Custom prompt + optional system override | Text response |
| `explain_diagnosis(fault, anomaly, tti, ...)` | Raw ML prediction dict | Natural language diagnosis |
| `analyse_timeseries(forecast_data)` | Forecaster output | Trend analysis |
| `answer_query(question, context)` | User question + RAG context | Contextual answer |
| `generate_incident_report(predict_result)` | Full prediction result | Structured incident report |
| `health()` | - | Latency check |

## Configuration (env vars)

| Variable | Default | Description |
|----------|---------|-------------|
| `NOC_LLM_MODEL` | `qwen3:8b` | Ollama model name |
| `NOC_MAX_TOKENS` | `4096` | Max generation length |
| `NOC_TEMPERATURE` | `0.7` | Generation temperature |

## Related

- [[rag-pipeline]] — Provides RAG context for queries
- [[noc-copilot]] — `/explain` and `/query` endpoints use this
- [[air-gap-validation]] — LLM tested offline
