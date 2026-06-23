#!/usr/bin/env python3
"""
Synthetic Network Telemetry Data Generator for PS13 Project.
Generates realistic time-series telemetry for an 11-router SD-WAN/MPLS network
across 4 sites (Bangalore, Mumbai, Chennai, Delhi) with configurable fault
injection. Output is a pandas DataFrame saved as parquet and CSV.

Fault types: link_fail, bgp_flap, congestion, route_leak, crc_errors,
             node_crash, lsp_break
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import warnings
import os

warnings.filterwarnings("ignore")

SEED = 42
N_HOURS = 720
START_DATE = datetime(2026, 1, 1, 0, 0)

DEVICES = {
    "CE1-BLR": {"site": "Bangalore", "role": "CE"},
    "PE1-BLR": {"site": "Bangalore", "role": "PE"},
    "P1-BLR": {"site": "Bangalore", "role": "P"},
    "CE1-MUM": {"site": "Mumbai", "role": "CE"},
    "PE1-MUM": {"site": "Mumbai", "role": "PE"},
    "P1-MUM": {"site": "Mumbai", "role": "P"},
    "CE1-CHE": {"site": "Chennai", "role": "CE"},
    "PE1-CHE": {"site": "Chennai", "role": "PE"},
    "CE1-DEL": {"site": "Delhi", "role": "CE"},
    "PE1-DEL": {"site": "Delhi", "role": "PE"},
    "P1-DEL": {"site": "Delhi", "role": "P"},
}

DEVICE_LIST = list(DEVICES.keys())
N_DEVICES = len(DEVICE_LIST)

FAULT_TYPES = [
    "link_fail",
    "bgp_flap",
    "congestion",
    "route_leak",
    "crc_errors",
    "node_crash",
    "lsp_break",
]

DEVICE_PAIRS = [
    ("CE1-BLR", "PE1-BLR"),
    ("CE1-MUM", "PE1-MUM"),
    ("CE1-CHE", "PE1-CHE"),
    ("CE1-DEL", "PE1-DEL"),
    ("PE1-BLR", "P1-BLR"),
    ("PE1-MUM", "P1-MUM"),
    ("PE1-DEL", "P1-DEL"),
]

PAIR_MAP = {}
for a, b in DEVICE_PAIRS:
    PAIR_MAP[a] = b
    PAIR_MAP[b] = a

FLOAT_METRICS = [
    "cpu_util_pct",
    "memory_util_pct",
    "interface_bandwidth_util_pct",
    "latency_ms",
    "packet_loss_pct",
    "jitter_ms",
    "tcp_retransmits_pct",
]

INT_METRICS = [
    "bgp_prefix_count",
    "ospf_lsa_count",
    "ldp_label_count",
    "mpls_label_stack_depth",
    "flow_count",
]

ALL_METRICS = FLOAT_METRICS + INT_METRICS

DELTA_MAP = {
    "cpu_util_pct": "delta_cpu",
    "latency_ms": "delta_latency",
    "packet_loss_pct": "delta_packet_loss",
    "interface_bandwidth_util_pct": "delta_bandwidth",
    "bgp_prefix_count": "delta_bgp",
}

SEVERITY_MAP = {
    "link_fail": 2,
    "bgp_flap": 1,
    "congestion": 1,
    "route_leak": 2,
    "crc_errors": 1,
    "node_crash": 2,
    "lsp_break": 2,
}

ROLE_BASELINE = {
    "CE": {
        "cpu_start": (25, 5),
        "mem_start": (42, 5),
        "bw_start": (38, 8),
        "lat_start": (1.5, 0.3),
        "bgp_start": (120, 20),
        "ospf_start": (250, 30),
        "ldp_start": (80, 15),
        "stack_depth": 2,
        "flow_start": (3000, 500),
    },
    "PE": {
        "cpu_start": (30, 5),
        "mem_start": (48, 5),
        "bw_start": (45, 8),
        "lat_start": (0.8, 0.3),
        "bgp_start": (180, 20),
        "ospf_start": (300, 30),
        "ldp_start": (110, 15),
        "stack_depth": 3,
        "flow_start": (6000, 500),
    },
    "P": {
        "cpu_start": (35, 5),
        "mem_start": (55, 5),
        "bw_start": (55, 8),
        "lat_start": (0.3, 0.3),
        "bgp_start": (80, 20),
        "ospf_start": (350, 30),
        "ldp_start": (130, 15),
        "stack_depth": 3,
        "flow_start": (8000, 500),
    },
}


def _random_walk(n, start, scale, lower=0, upper=100, mean_revert=0.02, diurnal_amp=0):
    """Generate a mean-reverting random walk time series."""
    changes = np.random.normal(0, scale, n)
    walk = np.zeros(n)
    walk[0] = start
    for i in range(1, n):
        revert = mean_revert * (start - walk[i - 1])
        walk[i] = walk[i - 1] + changes[i] + revert
    walk = np.clip(walk, lower, upper)
    if diurnal_amp > 0:
        diurnal = diurnal_amp * np.sin(2 * np.pi * np.arange(n) / 24 - np.pi / 2)
        walk = np.clip(walk + diurnal, lower, upper)
    return walk


def generate_baseline():
    """Generate clean baseline telemetry for all devices over N_HOURS."""
    np.random.seed(SEED)
    timestamps = [START_DATE + timedelta(hours=h) for h in range(N_HOURS)]

    device_params = {}
    for d_idx, device_id in enumerate(DEVICE_LIST):
        info = DEVICES[device_id]
        role = info["role"]
        bl = ROLE_BASELINE[role]
        np.random.seed(SEED + d_idx * 1000)

        cpu_start = bl["cpu_start"][0] + np.random.uniform(-bl["cpu_start"][1], bl["cpu_start"][1])
        mem_start = bl["mem_start"][0] + np.random.uniform(-bl["mem_start"][1], bl["mem_start"][1])
        bw_start = bl["bw_start"][0] + np.random.uniform(-bl["bw_start"][1], bl["bw_start"][1])
        lat_start = bl["lat_start"][0] + np.random.uniform(-bl["lat_start"][1], bl["lat_start"][1])
        loss_start = np.random.uniform(0, 0.05)
        jitter_start = np.random.uniform(0.05, 0.3)
        bgp_start = float(bl["bgp_start"][0] + np.random.randint(-bl["bgp_start"][1], bl["bgp_start"][1]))
        ospf_start = float(bl["ospf_start"][0] + np.random.randint(-bl["ospf_start"][1], bl["ospf_start"][1]))
        ldp_start = float(bl["ldp_start"][0] + np.random.randint(-bl["ldp_start"][1], bl["ldp_start"][1]))
        tcp_start = np.random.uniform(0, 0.2)
        flow_start = float(bl["flow_start"][0] + np.random.randint(-bl["flow_start"][1], bl["flow_start"][1]))

        device_params[device_id] = {
            "cpu": _random_walk(N_HOURS, cpu_start, 2.0, 0, 100, 0.01, diurnal_amp=5),
            "mem": _random_walk(N_HOURS, mem_start, 1.5, 10, 95, 0.01),
            "bw": _random_walk(N_HOURS, bw_start, 3.0, 0, 100, 0.01, diurnal_amp=10),
            "lat": _random_walk(N_HOURS, lat_start, 0.1, 0.05, 5.0, 0.01),
            "loss": _random_walk(N_HOURS, loss_start, 0.01, 0, 0.5, 0.01),
            "jitter": _random_walk(N_HOURS, jitter_start, 0.03, 0.01, 1.0, 0.01),
            "bgp": _random_walk(N_HOURS, bgp_start, 5.0, 50, 300, 0.01),
            "ospf": _random_walk(N_HOURS, ospf_start, 8.0, 150, 500, 0.01),
            "ldp": _random_walk(N_HOURS, ldp_start, 4.0, 30, 200, 0.01),
            "tcp": _random_walk(N_HOURS, tcp_start, 0.05, 0, 1.0, 0.01),
            "flow": _random_walk(N_HOURS, flow_start, 200, 500, 15000, 0.01),
            "stack_depth": bl["stack_depth"],
        }

    records = []
    for h in range(N_HOURS):
        for device_id in DEVICE_LIST:
            p = device_params[device_id]
            records.append(
                {
                    "hour": h,
                    "timestamp": timestamps[h],
                    "device_id": device_id,
                    "site": DEVICES[device_id]["site"],
                    "device_role": DEVICES[device_id]["role"],
                    "cpu_util_pct": round(float(p["cpu"][h]), 2),
                    "memory_util_pct": round(float(p["mem"][h]), 2),
                    "interface_bandwidth_util_pct": round(float(p["bw"][h]), 2),
                    "latency_ms": round(float(p["lat"][h]), 4),
                    "packet_loss_pct": round(float(p["loss"][h]), 4),
                    "jitter_ms": round(float(p["jitter"][h]), 4),
                    "bgp_prefix_count": int(round(p["bgp"][h])),
                    "ospf_lsa_count": int(round(p["ospf"][h])),
                    "ldp_label_count": int(round(p["ldp"][h])),
                    "mpls_label_stack_depth": p["stack_depth"],
                    "tcp_retransmits_pct": round(float(p["tcp"][h]), 4),
                    "flow_count": int(round(p["flow"][h])),
                    "fault_type": "none",
                    "fault_severity": 0,
                }
            )

    return pd.DataFrame(records)


def schedule_fault_events():
    """Generate a list of fault events.

    Each event is (device_idx, start_hour, end_hour, fault_type, severity).
    Targets ~8-12% of total device-hours with fault coverage.
    """
    np.random.seed(SEED + 999)
    events = []

    for device_idx in range(N_DEVICES):
        device_id = DEVICE_LIST[device_idx]
        h = 0
        while h < N_HOURS:
            if np.random.random() < 0.022:
                duration = np.random.randint(2, 9)
                end = min(h + duration, N_HOURS)
                fault_type = np.random.choice(FAULT_TYPES)
                severity = SEVERITY_MAP[fault_type]

                events.append((device_idx, h, end, fault_type, severity))

                if fault_type == "link_fail" and device_id in PAIR_MAP:
                    paired = PAIR_MAP[device_id]
                    paired_idx = DEVICE_LIST.index(paired)
                    events.append((paired_idx, h, end, "link_fail", severity))

                h = end
            else:
                h += 1

    return events


def apply_faults(df, events):
    """Inject fault signatures into the telemetry data."""
    df = df.copy()

    for device_idx, start, end, fault_type, severity in events:
        device_id = DEVICE_LIST[device_idx]
        role = DEVICES[device_id]["role"]

        mask = (df["device_id"] == device_id) & (df["hour"] >= start) & (df["hour"] < end)
        n = mask.sum()
        if n == 0:
            continue

        idx = np.where(mask)[0]

        if fault_type == "link_fail":
            df.loc[mask, "interface_bandwidth_util_pct"] = np.round(
                np.random.uniform(0, 2, n), 2
            )
            df.loc[mask, "latency_ms"] = np.round(
                np.random.uniform(50, 200, n), 4
            )
            df.loc[mask, "packet_loss_pct"] = np.round(
                np.random.uniform(20, 100, n), 4
            )
            df.loc[mask, "tcp_retransmits_pct"] = np.round(
                np.random.uniform(5, 30, n), 4
            )
            df.loc[mask, "jitter_ms"] = np.round(
                np.random.uniform(5, 20, n), 4
            )

        elif fault_type == "bgp_flap":
            df.loc[mask, "cpu_util_pct"] = np.round(
                np.random.uniform(60, 90, n), 2
            )
            df.loc[mask, "memory_util_pct"] = np.round(
                np.random.uniform(60, 85, n), 2
            )
            osc = np.sin(np.linspace(0, 8 * np.pi, n)) * 0.5 + 0.5
            df.loc[mask, "bgp_prefix_count"] = (50 + osc * 250).astype(int)

        elif fault_type == "congestion":
            df.loc[mask, "interface_bandwidth_util_pct"] = np.round(
                np.random.uniform(85, 98, n), 2
            )
            df.loc[mask, "latency_ms"] = np.round(
                np.random.uniform(10, 50, n), 4
            )
            df.loc[mask, "packet_loss_pct"] = np.round(
                np.random.uniform(0.5, 5, n), 4
            )
            df.loc[mask, "tcp_retransmits_pct"] = np.round(
                np.random.uniform(3, 15, n), 4
            )

        elif fault_type == "route_leak":
            df.loc[mask, "bgp_prefix_count"] = np.random.randint(200, 500, n)
            df.loc[mask, "latency_ms"] = np.round(
                np.random.uniform(5, 30, n), 4
            )
            df.loc[mask, "cpu_util_pct"] = np.round(
                np.random.uniform(50, 75, n), 2
            )
            df.loc[mask, "memory_util_pct"] = np.round(
                np.random.uniform(55, 75, n), 2
            )

        elif fault_type == "crc_errors":
            df.loc[mask, "packet_loss_pct"] = np.round(
                np.random.uniform(1, 10, n), 4
            )
            df.loc[mask, "tcp_retransmits_pct"] = np.round(
                np.random.uniform(5, 20, n), 4
            )
            df.loc[mask, "jitter_ms"] = np.round(
                np.random.uniform(1, 10, n), 4
            )

        elif fault_type == "node_crash":
            half = n // 2
            first = idx[:half]
            second = idx[half:]

            for col in FLOAT_METRICS:
                df.loc[first, col] = np.nan
            for col in INT_METRICS:
                df.loc[first, col] = 0

            if len(second) > 0:
                recovery_pct = {"CE": 0.30, "PE": 0.35, "P": 0.40}[role]
                crash_baseline = {
                    "cpu_util_pct": 30,
                    "memory_util_pct": 48,
                    "interface_bandwidth_util_pct": 45,
                    "latency_ms": 1.0,
                    "packet_loss_pct": 0.05,
                    "jitter_ms": 0.2,
                    "tcp_retransmits_pct": 0.1,
                    "bgp_prefix_count": 120,
                    "ospf_lsa_count": 280,
                    "ldp_label_count": 100,
                    "mpls_label_stack_depth": 2,
                    "flow_count": 5000,
                }
                for col in FLOAT_METRICS:
                    b = crash_baseline[col]
                    df.loc[second, col] = np.round(
                        np.random.uniform(0, b * recovery_pct, len(second)), 4
                    )
                for col in INT_METRICS:
                    b = crash_baseline[col]
                    vals = np.random.uniform(0, b * recovery_pct, len(second))
                    df.loc[second, col] = np.round(vals).astype(int)

        elif fault_type == "lsp_break":
            df.loc[mask, "mpls_label_stack_depth"] = np.where(
                np.random.random(n) < 0.6, 0, 1
            )
            df.loc[mask, "packet_loss_pct"] = np.round(
                np.random.uniform(5, 50, n), 4
            )
            df.loc[mask, "latency_ms"] = np.round(
                np.random.uniform(20, 100, n), 4
            )
            df.loc[mask, "jitter_ms"] = np.round(
                np.random.uniform(5, 20, n), 4
            )

        df.loc[mask, "fault_type"] = fault_type
        df.loc[mask, "fault_severity"] = severity

    return df


def add_engineered_features(df):
    """Add lag features, rolling statistics, and delta features.

    All computed per-device to prevent cross-device leakage.
    """
    df = df.sort_values(["device_id", "hour"]).reset_index(drop=True)

    for lag in [1, 3, 6, 12]:
        for col in ALL_METRICS:
            df[f"{col}_lag_{lag}"] = df.groupby("device_id")[col].shift(lag)

    for col in ALL_METRICS:
        grouped = df.groupby("device_id")[col]
        df[f"{col}_rolling_mean_6"] = grouped.transform(
            lambda x: x.rolling(6, min_periods=1).mean()
        )
        df[f"{col}_rolling_std_6"] = grouped.transform(
            lambda x: x.rolling(6, min_periods=1).std()
        )
        df[f"{col}_rolling_max_6"] = grouped.transform(
            lambda x: x.rolling(6, min_periods=1).max()
        )

    for col, delta_name in DELTA_MAP.items():
        df[delta_name] = df.groupby("device_id")[col].diff()

    return df


def compute_time_to_incident(df, events):
    """Calculate hours until the next fault for every sample.

    Samples within a fault window get time_to_incident_hours = 0.
    Samples with no future fault get (N_HOURS - current_hour).
    """
    device_windows = {}
    for device_idx, start, end, _, _ in events:
        device_id = DEVICE_LIST[device_idx]
        device_windows.setdefault(device_id, []).append((start, end))

    tti = np.full(len(df), np.nan, dtype=float)

    for device_id in DEVICE_LIST:
        mask = df["device_id"] == device_id
        hours = df.loc[mask, "hour"].values
        windows = sorted(device_windows.get(device_id, []))
        positions = np.where(mask)[0]

        for i, h in enumerate(hours):
            val = float(N_HOURS - h)
            for sh, eh in windows:
                if sh <= h < eh:
                    val = 0.0
                    break
                elif h < sh:
                    val = float(sh - h)
                    break
            tti[positions[i]] = val

    df["time_to_incident_hours"] = tti
    return df


def print_summary(df):
    """Print summary statistics of the generated dataset."""
    n_faults = (df["fault_type"] != "none").sum()
    total = len(df)
    n_devices = df["device_id"].nunique()
    n_sites = df["site"].nunique()

    print(f"{'=' * 60}")
    print(f"  PS13 Synthetic Telemetry Dataset Summary")
    print(f"{'=' * 60}")
    print(f"  Samples:          {total:,}")
    print(f"  Devices:          {n_devices}")
    print(f"  Sites:            {n_sites}")
    print(f"  Date Range:       {df['timestamp'].min()} to {df['timestamp'].max()}")
    print(f"  Duration:         {N_HOURS} hours ({N_HOURS // 24} days)")
    print(f"  Fault Samples:    {n_faults:,} ({100 * n_faults / total:.1f}%)")
    print(f"  Clean Samples:    {total - n_faults:,} ({100 * (total - n_faults) / total:.1f}%)")
    print()

    fault_subset = df[df["fault_type"] != "none"]
    if len(fault_subset) > 0:
        print("  Fault Distribution:")
        fault_counts = fault_subset["fault_type"].value_counts()
        for ft, cnt in fault_counts.items():
            print(f"    {ft:15s}: {cnt:5d} ({100 * cnt / n_faults:.1f}%)")
        print()

    print(f"  Feature Columns:  {len(df.columns)}")
    size_kb = df.memory_usage(deep=True).sum() / 1024
    print(f"  Memory:           {size_kb:.1f} KB")
    print()

    summary_cols = [
        "cpu_util_pct",
        "latency_ms",
        "packet_loss_pct",
        "interface_bandwidth_util_pct",
        "bgp_prefix_count",
    ]
    print("  Key Metrics Summary (all samples, NaN excluded):")
    print(f"  {'Metric':<35s} {'Mean':>8s} {'Std':>8s} {'Min':>8s} {'Max':>8s}")
    print(f"  {'-' * 35} {'-' * 8} {'-' * 8} {'-' * 8} {'-' * 8}")
    for col in summary_cols:
        s = df[col].dropna()
        print(
            f"  {col:<35s} {s.mean():>8.2f} {s.std():>8.2f} {s.min():>8.2f} {s.max():>8.2f}"
        )

    print()
    print("  Time-to-Incident Stats:")
    tti = df["time_to_incident_hours"].dropna()
    print(f"    Mean: {tti.mean():.1f}h  Median: {tti.median():.1f}h  "
          f"Zero (in fault): {(tti == 0).sum():,}")
    print(f"{'=' * 60}")


def main(n_hours=720):
    """Generate synthetic telemetry data and save to disk.

    Args:
        n_hours: Number of hourly samples to generate (default 720 = 30 days).

    Returns:
        pd.DataFrame with the generated telemetry data.
    """
    global N_HOURS
    N_HOURS = n_hours

    print("Generating baseline telemetry...")
    df = generate_baseline()

    print("Scheduling fault events...")
    events = schedule_fault_events()
    print(f"  Generated {len(events)} fault event windows")

    print("Injecting fault signatures...")
    df = apply_faults(df, events)

    print("Adding engineered features (lags, rolling stats, deltas)...")
    df = add_engineered_features(df)

    print("Computing time-to-incident...")
    df = compute_time_to_incident(df, events)

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(output_dir, exist_ok=True)

    parquet_path = os.path.join(output_dir, "telemetry.parquet")
    csv_path = os.path.join(output_dir, "telemetry.csv")

    print(f"\nSaving to {parquet_path} ...")
    df.to_parquet(parquet_path, index=False)

    print(f"Saving to {csv_path} ...")
    df.to_csv(csv_path, index=False)
    csv_size = os.path.getsize(csv_path) / (1024 * 1024)
    print(f"  CSV size: {csv_size:.2f} MB")

    print()
    print_summary(df)

    return df


if __name__ == "__main__":
    df = main()
