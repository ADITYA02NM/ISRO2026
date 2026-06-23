# Future — PS13 SSD Boot Delivery Product

## Vision

**PS13 delivered as a bootable USB SSD** — plug into any x86_64 laptop (RTX 4060 or better), boot from USB, and get a fully operational air-gapped NOC copilot in minutes. No OS install, no dependency setup, no internet.

The SSD becomes the **product delivery vehicle**: one-time build, infinite replication via `dd`, field-deployable by non-technical operators.

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    USB SSD (Bootable)                             │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Arch Linux (minimal, hardened)                           │   │
│  │  • systemd-boot (UEFI)                                    │   │
│  │  • systemd-networkd (all interfaces DOWN at boot)          │   │
│  │  • No X11/Wayland by default (TTY-only unless Tauri runs) │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Core Services (auto-start via systemd)                   │   │
│  │  • Containerlab + FRR (4-site topology)                   │   │
│  │  • Prometheus + Kafka + Telegraf                          │   │
│  │  • Ollama + Qwen3-8B + ChromaDB                          │   │
│  │  • ML inference pipeline (7 ONNX models)                  │   │
│  │  • T3 — FastAPI backend + WebSocket bridge                │   │
│  │  • T2 — Served dashboard (ECharts + anime)                │   │
│  │  • T1 — Served operator console (Three.js + anime)        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Tauri Desktop App (controller)                           │   │
│  │  • Start / stop / restart all services                    │   │
│  │  • Health monitoring (CPU/GPU/RAM/temperature)            │   │
│  │  • Log viewer (tail -f for each service)                  │   │
│  │  • GPU detection & driver status                          │   │
│  │  • First-boot setup wizard                                │   │
│  │  • Ability to create new instances of PS13 Device Groups  │   │
│  │  • Air-gap compliance scanner (one-click)                 │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Persistent Storage                                        │   │
│  │  • /var/lib/containerlab — Docker image cache             │   │
│  │  • /var/lib/ollama — model storage (Qwen3 GGUF)           │   │
│  │  • /var/lib/chromadb — vector database                    │   │
│  │  • /opt/ps13/data — telemetry archives, ML model exports  │   │
│  │  • /opt/ps13/config — network configs, device definitions │   │
│  │  • /opt/ps13/logs — all service logs (journald + files)   │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

---

## First-Boot Flow

```
┌──────────────────────────────────────────────────────┐
│ 1. Insert SSD → Boot from USB (BIOS boot menu)       │
│    • systemd-boot menu (3s timeout → default)        │
│    • "PS13 NOC Copilot — Air-Gapped"                 │
│    • "PS13 — Recovery / Safe Mode"                   │
│    • "PS13 — Memory Test"                            │
└──────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────┐
│ 2. Kernel boots → systemd starts                      │
│    • All network interfaces DOWN at boot              │
│    • No DHCP, no DNS — air-gap enforced               │
│    • tmpfs on /tmp, /run                              │
│    • Mount overlay for root (read-only squashfs)      │
│    • Persistent data partition mounted (LUKS)         │
└──────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────┐
│ 3. startup.setup.service → First-boot TTY wizard     │
│    • This runs only on first boot                     │
│    • Detects GPU: NVIDIA / AMD / Intel / None (CPU)   │
│    • If NVIDIA: installs matching driver (see below)  │
│    • Prompts: Model tier (Q4 / Q5 / Q8)              │
│    • Prompts: Topology scale (4-site / 8-site)        │
│    • Prompts: Enable LLM copilot (yes/no — CPU skip) │
│    • Writes /opt/ps13/config/setup.json              │
└──────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────┐
│ 4. startup.ps13.service → Launch all services         │
│    • Docker daemon → pull container images (from cache)│
│    • Containerlab → deploy topology                   │
│    • Prometheus + Telegraf → start telemetry pipeline │
│    • Ollama → load model (Qwen3-8B.Q4_K_M.gguf)       │
│    • ChromaDB → load RAG index                        │
│    • ML runner → start inference pipeline             │
│    • T3 → FastAPI + WebSocket server                  │
│    • T2 + T1 → serve frontends                        │
│    • Tauri app → launch (if GPU available)            │
│    • System ready notification (beep / LED)           │
└──────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────┐
│ 5. Tauri App (or TTY fallback) — Control Center       │
│    Service              Status  Actions                │
│    ──────────────────────────────────────              │
│    Containerlab         ● Running  [Restart] [Stop]   │
│    Telemetry Pipeline   ● Running  [Restart] [Stop]   │
│    Ollama (Qwen3)       ● Running  [Switch Model]     │
│    ML Inference         ● Running  [Restart] [Stop]   │
│    T3 Backend           ● Running  [Restart] [Stop]   │
│    T2 Dashboard         ● Running  [Open Browser]     │
│    T1 Console           ● Running  [Open Browser]     │
│    ──────────────────────────────────────              │
│    Air-Gap:   ✓ COMPLIANT   [Full Scan]               │
│    GPU Temp:  62°C          VRAM: 5.8/8.0 GB          │
│    CPU Load:  34%           RAM:  8.2/15.6 GB         │
└──────────────────────────────────────────────────────┘
```

---

## GPU Driver Strategy (TBD)

**Challenge:** The SSD must boot on laptops with *any* NVIDIA GPU generation (RTX 20xx, 30xx, 40xx, 50xx), each requiring different driver versions.

| Approach | Pros | Cons |
|----------|------|------|
| **Bundle latest NVIDIA driver** | Works for 40xx/50xx | Fails for older GPUs (20xx/30xx with different API) |
| **Bundle multiple driver versions** | Covers all generations ~180 MB each | ~1 GB storage, complex auto-detection |
| **modprobe + firmware only (nouveau)** | Works on everything, fits in 10 MB | No CUDA → no LLM/ML acceleration |
| **Container-based GPU passthrough** | Host-agnostic, Docker NVIDIA toolkit | Requires nvidia-docker on host |
| **Wizard installs driver at first boot** | Ensures latest compatible version | Requires host to be online (violates air-gap?) |

**Likely path:** Bundle 3 driver versions (525-series for 30xx, 535-series for 40xx, 550-series for 50xx) with auto-detection at first boot. Pre-cached offline. Nouveau fallback for unrecognized GPUs (CPU-only mode).

---

## Tauri Desktop App Design (TBD)

The controller app is built with [Tauri](https://tauri.app) (Rust backend + web frontend).

### Planned Features

| Feature | Priority | Status |
|---------|----------|--------|
| Service lifecycle (start/stop/restart) | P0 | TBD |
| Health dashboard (CPU/GPU/RAM/disk) | P0 | TBD |
| Real-time log viewer (per-service) | P0 | TBD |
| Air-gap compliance scan (one-click) | P0 | TBD |
| First-boot setup wizard | P0 | TBD |
| GPU detection + driver check | P0 | TBD |
| Topology viewer (simplified) | P1 | TBD |
| SSH into Containerlab nodes | P1 | TBD |
| Backup / restore configuration | P1 | TBD |
| Firmware update (SSD reflash over USB) | P2 | TBD |

### Architecture

```
┌───────────────────────────────────────┐
│         Tauri Shell (Rust)            │
│  • systemd D-Bus client               │
│  • process supervisor (cgroups)       │
│  • health polling (sysinfo crate)     │
│  • GPU detection (NVML bindings)      │
└─────────────┬─────────────────────────┘
              │ IPC (http://localhost:9080)
┌─────────────▼─────────────────────────┐
│         Web Frontend (React)          │
│  • Dashboard panels                   │
│  • Service card grid                  │
│  • Log view (terminal emulator)       │
│  • Setup wizard (multi-step)          │
│  • Build a new Instance wizard        │
│  • Terminal SSH viewer (xterm.js)     │
└───────────────────────────────────────┘
```

---

## Boot Target Hardware

| Tier | GPU | Max Models | Use Case |
|------|-----|-----------|----------|
| **Full** | RTX 4060 (8GB) | Qwen3-8B + 7 ML | Full copilot + prediction |
| **Medium** | RTX 3050 (4GB) | Qwen3-4B + 5 ML | Prediction without LLM |
| **CPU** | Intel/AMD iGPU | 0 | Rule engine only (no ML) |
| **Any** | Unrecognized GPU | 0 | Rule engine + basic alerts |

---

## Storage Layout

```
/dev/sda1 → 512 MB EFI (vfat) — systemd-boot, kernels, initramfs
/dev/sda2 → 32 GB  ROOT (squashfs, dm-verity) — base Arch + system
/dev/sda3 → 128 GB DATA (btrfs, LUKS) — persistent artifacts
  ├── @docker     → /var/lib/docker
  ├── @ollama     → /var/lib/ollama (Qwen3 GGUF ~5.5 GB)
  ├── @chromadb   → /var/lib/chromadb
  ├── @prometheus → /var/lib/prometheus
  ├── @ps13       → /opt/ps13
  │   ├── config/    → setup.json, network topologies, device definitions
  │   ├── data/      → telemetry archives, ML model exports
  │   ├── logs/      → all service logs
  │   ├── models/    → ONNX exported models (7 models ~200 MB)
  │   └── runbooks/  → 50+ ChromaDB source documents
  └── @home      → /home (user data)
```

**Total estimate:** ~32 GB root (fixed) + ~100-150 GB data (grows with telemetry).

---

## Boot Support (TBD)

| Scenario | Status |
|----------|--------|
| UEFI x86_64 | ✅ Supported (systemd-boot) |
| Legacy BIOS | ❌ TBD (GRUB fallback?) |
| Secure Boot | ❌ TBD (MOK enrollment flow?) |
| Apple Silicon | ❌ Not supported (different boot model, no NVIDIA) |
| ARM64 (Raspberry Pi 5) | ❌ TBD (reduced topology, CPU-only) |

---

## "Antenna" Concept (TBD)

> **Note:** The "antenna" concept was mentioned during planning but its exact meaning was not clarified. Possible interpretations:

| Interpretation | Description |
|----------------|-------------|
| **Physical antenna** | External USB Wi-Fi dongle for passive spectrum monitoring / signal detection in the NOC environment |
| **Radiated emissions monitor** | Side-channel detection — antenna picks up electromagnetic leakage from network equipment for non-invasive health monitoring |
| **Wireless sensor node** | ESP32-based remote sensor that feeds telemetry (temperature, humidity, vibration) into PS13 via a serial/Bluetooth bridge |
| **Tauri app feature codename** | Some as-yet-undefined feature in the desktop controller app called "Antenna" — perhaps a notification broadcast system |
| **Data exfiltration watchdog** | Antenna-shaped concept that monitors for unauthorized wireless signals leaving the air-gapped environment |

**Clarification needed — this section should be updated once the intent is known.**

---

## Roadmap

| Phase | Milestone | Dependencies |
|-------|-----------|-------------|
| **P0** | Run & validate PS13 end-to-end from this repo | This repo (in progress) |
| **P1** | Build Arch Linux minimal image | [archiso](https://wiki.archlinux.org/title/archiso) |
| **P2** | Containerize all services as systemd units | P1 |
| **P3** | First-boot TTY setup wizard | P1 |
| **P4** | Tauri desktop app (core loop) | P1-P3 |
| **P5** | GPU driver bundling + auto-detection | P1 |
| **P6** | LUKS + dm-verity hardening | P1 |
| **P7** | Production SSD build + `dd` deployment script | P0-P6 |
| **P8** | Field testing on RTX 4060, 3050, CPU-only laptops | P7 |
| **P9** | "Antenna" integration | TBD |

---

## Questions Still Open

1. **GPU driver bundling** — which NVIDIA driver versions to bundle? What about AMD ROCm?
2. **Tauri app** — Web UI framework? (React/Vue/Svelte?) System tray vs full window?
3. **UEFI-only or Legacy BIOS too?** — Legacy BIOS adds GRUB complexity.
4. **Secure Boot** — MOK enrollment flow or disablement instructions?
5. **"Antenna"** — What does this mean?
6. **Licensing** — GPL implications of bundling Arch? All Docker images need offline caching.
7. **Updates** — How does the user update the SSD? Reflash from ISO? Over-the-air (violates air-gap)?
