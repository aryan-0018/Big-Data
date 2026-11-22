"""
Real-Time Patient Vital Signs Monitoring Engine using Apache Flink Architecture.
Simulates stateful stream processing, watermarks, sliding and tumbling windows,
clinical threshold detection, and multi-vital alert generation.
(Educational and demonstration purposes; synthetic data).
"""

import os
import json
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="tab10")
plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 11})

os.makedirs("activity3_flink", exist_ok=True)
os.makedirs("visualizations", exist_ok=True)

# ---------------------------------------------------------------------
# PATIENT COHORT CONFIGURATION
# ---------------------------------------------------------------------
PATIENTS = [
    {"patient_id": "PT-01", "name": "Rajesh Sharma", "age": 64, "ward": "ICU-A", "bed": "Bed-101", "condition": "Post-cardiac bypass"},
    {"patient_id": "PT-02", "name": "Sunita Patil", "age": 52, "ward": "ICU-A", "bed": "Bed-102", "condition": "Acute pneumonia"},
    {"patient_id": "PT-03", "name": "David Miller", "age": 71, "ward": "ICU-B", "bed": "Bed-201", "condition": "Severe sepsis recovery"},
    {"patient_id": "PT-04", "name": "Amina Begum", "age": 45, "ward": "ICU-B", "bed": "Bed-202", "condition": "Post-thoracic surgery"},
    {"patient_id": "PT-05", "name": "Venkatesh Rao", "age": 59, "ward": "Step-Down", "bed": "Bed-301", "condition": "Cardiomyopathy"},
    {"patient_id": "PT-06", "name": "Elena Rostova", "age": 38, "ward": "Step-Down", "bed": "Bed-302", "condition": "COPD exacerbation"},
    {"patient_id": "PT-07", "name": "Karthik Verma", "age": 67, "ward": "CCU", "bed": "Bed-401", "condition": "Myocardial infarction"},
    {"patient_id": "PT-08", "name": "Fatima Zahra", "age": 49, "ward": "CCU", "bed": "Bed-402", "condition": "Post-operative monitoring"}
]

# Educational Clinical Thresholds
THRESHOLDS = {
    "HR_HIGH_CRITICAL": 125,
    "HR_HIGH_WARNING": 105,
    "HR_LOW_CRITICAL": 45,
    "HR_LOW_WARNING": 55,
    "SPO2_CRITICAL": 90.0,
    "SPO2_WARNING": 93.0,
    "TEMP_HIGH_CRITICAL": 39.0,
    "TEMP_HIGH_WARNING": 38.3,
    "TEMP_LOW_CRITICAL": 35.0
}

# ---------------------------------------------------------------------
# STREAM ENGINE (FLINK JOB SIMULATOR WITH WATERMARK & WINDOW STATE)
# ---------------------------------------------------------------------
class FlinkStreamProcessor:
    """Simulates Flink KeyedStream processing with Sliding Windows & State."""
    def __init__(self, window_size_sec=30, slide_sec=10):
        self.window_size_sec = window_size_sec
        self.slide_sec = slide_sec
        # State per patient: list of (timestamp_dt, event_dict)
        self.patient_state = {}

    def process_telemetry_stream(self, telemetry_events):
        alerts = []
        window_summaries = []

        # Sort events by timestamp to ensure event-time ordering (watermark simulated)
        events_sorted = sorted(telemetry_events, key=lambda x: x["timestamp"])

        for ev in events_sorted:
            pid = ev["patient_id"]
            ev_dt = datetime.fromisoformat(ev["timestamp"])
            
            if pid not in self.patient_state:
                self.patient_state[pid] = []
            
            # Append to patient event buffer
            self.patient_state[pid].append((ev_dt, ev))

            # 1. Instantaneous Threshold Evaluation (MapFunction & FlatMapFunction)
            hr = ev["heart_rate_bpm"]
            spo2 = ev["spo2_pct"]
            temp = ev["temperature_c"]
            
            critical_flags = []
            warning_flags = []

            # Heart rate
            if hr >= THRESHOLDS["HR_HIGH_CRITICAL"]:
                critical_flags.append(f"Severe Tachycardia ({hr} bpm)")
            elif hr <= THRESHOLDS["HR_LOW_CRITICAL"]:
                critical_flags.append(f"Severe Bradycardia ({hr} bpm)")
            elif hr >= THRESHOLDS["HR_HIGH_WARNING"]:
                warning_flags.append(f"Mild Tachycardia ({hr} bpm)")
            elif hr <= THRESHOLDS["HR_LOW_WARNING"]:
                warning_flags.append(f"Mild Bradycardia ({hr} bpm)")

            # SpO2
            if spo2 <= THRESHOLDS["SPO2_CRITICAL"]:
                critical_flags.append(f"Critical Hypoxemia ({spo2:.1f}%)")
            elif spo2 <= THRESHOLDS["SPO2_WARNING"]:
                warning_flags.append(f"Mild Desaturation ({spo2:.1f}%)")

            # Temperature
            if temp >= THRESHOLDS["TEMP_HIGH_CRITICAL"]:
                critical_flags.append(f"Severe Hyperthermia ({temp:.1f}°C)")
            elif temp <= THRESHOLDS["TEMP_LOW_CRITICAL"]:
                critical_flags.append(f"Hypothermia ({temp:.1f}°C)")
            elif temp >= THRESHOLDS["TEMP_HIGH_WARNING"]:
                warning_flags.append(f"Pyrexia/Fever ({temp:.1f}°C)")

            # Composite multi-vital trigger (e.g. Hypoxia + Tachycardia indicates shock/respiratory distress)
            if spo2 <= 91.0 and hr >= 115:
                critical_flags.append(f"COMPOSITE: Acute Cardiorespiratory Distress ({spo2:.1f}% SpO2 & {hr} bpm)")

            if critical_flags:
                severity = "CRITICAL_RED"
                alert_type = "; ".join(critical_flags)
            elif warning_flags:
                severity = "URGENT_YELLOW"
                alert_type = "; ".join(warning_flags)
            else:
                severity = None

            if severity:
                alerts.append({
                    "alert_id": f"FLK-ALT-{pid}-{len(alerts)+1:04d}",
                    "patient_id": pid,
                    "patient_name": ev["patient_name"],
                    "ward": ev["ward"],
                    "bed": ev["bed"],
                    "timestamp": ev["timestamp"],
                    "severity": severity,
                    "condition_details": alert_type,
                    "heart_rate_bpm": hr,
                    "spo2_pct": spo2,
                    "temperature_c": temp,
                    "clinical_action": "Stat bedside review, notify attending intensivist, prepare arterial blood gas (ABG) panel." if severity == "CRITICAL_RED" else "Nurse check, re-evaluate vitals in 5 minutes."
                })

        # 2. Windowed Aggregations (Sliding Window: 30s window, 10s slide)
        for pid, history in self.patient_state.items():
            if not history:
                continue
            min_time = history[0][0]
            max_time = history[-1][0]
            
            cur_window_start = min_time
            while cur_window_start + timedelta(seconds=self.window_size_sec) <= max_time:
                cur_window_end = cur_window_start + timedelta(seconds=self.window_size_sec)
                
                # Filter events within window: [start, end)
                win_events = [e[1] for e in history if cur_window_start <= e[0] < cur_window_end]
                
                if win_events:
                    hr_vals = [e["heart_rate_bpm"] for e in win_events]
                    spo2_vals = [e["spo2_pct"] for e in win_events]
                    temp_vals = [e["temperature_c"] for e in win_events]
                    
                    p_info = win_events[0]
                    window_summaries.append({
                        "patient_id": pid,
                        "patient_name": p_info["patient_name"],
                        "ward": p_info["ward"],
                        "bed": p_info["bed"],
                        "window_start": cur_window_start.strftime("%Y-%m-%d %H:%M:%S"),
                        "window_end": cur_window_end.strftime("%Y-%m-%d %H:%M:%S"),
                        "sample_count": len(win_events),
                        "avg_hr": round(float(np.mean(hr_vals)), 1),
                        "max_hr": int(np.max(hr_vals)),
                        "min_hr": int(np.min(hr_vals)),
                        "avg_spo2": round(float(np.mean(spo2_vals)), 1),
                        "min_spo2": round(float(np.min(spo2_vals)), 1),
                        "avg_temp": round(float(np.mean(temp_vals)), 2),
                        "max_temp": round(float(np.max(temp_vals)), 2)
                    })

                cur_window_start += timedelta(seconds=self.slide_sec)

        return alerts, window_summaries

# ---------------------------------------------------------------------
# TELEMETRY GENERATOR
# ---------------------------------------------------------------------
def generate_patient_telemetry(num_steps=180, step_seconds=5):
    """Generates continuous streams with physiological profiles and induced critical events."""
    random.seed(42)
    np.random.seed(42)
    
    start_time = datetime(2025, 11, 10, 14, 0, 0)
    all_events = []

    for step in range(num_steps):
        t = start_time + timedelta(seconds=step * step_seconds)
        
        for p in PATIENTS:
            pid = p["patient_id"]
            
            # Baseline parameters
            base_hr = 76.0
            base_spo2 = 98.2
            base_temp = 36.8

            # Specific patient conditions
            # PT-02 develops acute hypoxemic episode during step 60-120
            if pid == "PT-02" and 60 <= step <= 120:
                spo2 = max(82.0, base_spo2 - (step - 60) * 0.35 + random.uniform(-1.0, 1.0))
                hr = base_hr + (step - 60) * 0.7 + random.uniform(-3, 3) # Compensatory tachycardia
                temp = base_temp + random.uniform(-0.1, 0.2)
            # PT-03 develops septic shock with high fever and tachycardia at step 80-140
            elif pid == "PT-03" and 80 <= step <= 140:
                spo2 = base_spo2 - random.uniform(1.0, 3.5)
                hr = min(142.0, base_hr + (step - 80) * 0.9 + random.uniform(-3, 4))
                temp = min(39.6, base_temp + (step - 80) * 0.05 + random.uniform(-0.1, 0.2))
            # PT-07 develops sudden severe bradycardia at step 90-110
            elif pid == "PT-07" and 90 <= step <= 110:
                spo2 = base_spo2 - random.uniform(0.5, 1.5)
                hr = max(42.0, base_hr - (step - 90) * 1.8 + random.uniform(-2, 2))
                temp = base_temp + random.uniform(-0.1, 0.1)
            else:
                # Normal stable variations
                hr = base_hr + random.uniform(-5.0, 6.0)
                spo2 = min(99.5, base_spo2 + random.uniform(-1.0, 1.0))
                temp = base_temp + random.uniform(-0.2, 0.2)

            event = {
                "patient_id": pid,
                "patient_name": p["name"],
                "ward": p["ward"],
                "bed": p["bed"],
                "timestamp": t.strftime("%Y-%m-%d %H:%M:%S"),
                "heart_rate_bpm": int(round(hr)),
                "spo2_pct": round(float(spo2), 1),
                "temperature_c": round(float(temp), 2)
            }
            all_events.append(event)

    return all_events

def run_flink_patient_analytics():
    print("=" * 70)
    print("STARTING ACTIVITY 3: APACHE FLINK REAL-TIME PATIENT HEALTH MONITORING")
    print("=" * 70)

    print("[Stream Generator] Simulating high-frequency patient physiological telemetry...")
    telemetry = generate_patient_telemetry(num_steps=180, step_seconds=5)
    print(f"✓ Generated {len(telemetry):,} telemetry records (15 minutes continuous monitoring).")

    # Save raw stream to CSV
    df_raw = pd.DataFrame(telemetry)
    df_raw.to_csv("activity3_flink/patient_telemetry_stream.csv", index=False)

    # Execute Flink stream processing engine
    flink_processor = FlinkStreamProcessor(window_size_sec=30, slide_sec=10)
    print("\n[Flink Execution Engine] Executing streaming DAG, watermarking & window operations...")
    alerts, summaries = flink_processor.process_telemetry_stream(telemetry)

    print(f"✓ Processed stream: Generated {len(alerts)} clinical alerts.")
    print(f"✓ Calculated {len(summaries)} sliding window state summaries.")

    # Save alerts to JSON
    with open("activity3_flink/patient_clinical_alerts.json", "w", encoding="utf-8") as f:
        json.dump(alerts, f, indent=2)

    # Save window summaries to CSV
    df_sum = pd.DataFrame(summaries)
    df_sum.to_csv("activity3_flink/patient_window_summary.csv", index=False)

    df_alerts = pd.DataFrame(alerts)
    alert_counts = df_alerts.groupby(["patient_id", "patient_name", "ward", "severity"]).size().unstack(fill_value=0)
    alert_counts["TOTAL"] = alert_counts.sum(axis=1)
    alert_counts = alert_counts.sort_values("TOTAL", ascending=False).reset_index()
    alert_counts.to_csv("activity3_flink/patient_alert_distribution.csv", index=False)

    print("\n[Patient Clinical Alert Summary]")
    print(alert_counts.to_string())

    # -----------------------------------------------------------------
    # VISUALIZATIONS GENERATION
    # -----------------------------------------------------------------
    print("\nGenerating Flink streaming analytics charts...")

    # Chart 1: Multi-Vital Time-Series for Acute Hypoxemia Episode (PT-02)
    df_pt2 = df_raw[df_raw["patient_id"] == "PT-02"].copy()
    df_pt2["dt"] = pd.to_datetime(df_pt2["timestamp"])

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8.5), sharex=True)

    # Panel 1: SpO2
    ax1.plot(df_pt2["dt"], df_pt2["spo2_pct"], color="#1f77b4", linewidth=2.2, label="SpO2 (%)")
    ax1.axhline(y=90, color="red", linestyle="--", linewidth=1.5, label="Critical Hypoxemia Threshold (90%)")
    ax1.axhline(y=93, color="orange", linestyle=":", linewidth=1.2, label="Warning Desaturation (93%)")
    ax1.fill_between(df_pt2["dt"], 80, 90, color="red", alpha=0.15)
    ax1.set_ylabel("SpO2 (%)", fontweight="bold")
    ax1.set_ylim(80, 101)
    ax1.legend(loc="lower left")
    ax1.set_title("Real-Time Patient Stream (PT-02): Acute Hypoxemic Desaturation Episode", fontsize=13, fontweight="bold")

    # Panel 2: Heart Rate
    ax2.plot(df_pt2["dt"], df_pt2["heart_rate_bpm"], color="#d62728", linewidth=2.2, label="Heart Rate (bpm)")
    ax2.axhline(y=105, color="orange", linestyle=":", linewidth=1.2, label="Mild Tachycardia (105 bpm)")
    ax2.axhline(y=125, color="red", linestyle="--", linewidth=1.5, label="Critical Tachycardia (125 bpm)")
    ax2.set_ylabel("Heart Rate (bpm)", fontweight="bold")
    ax2.set_ylim(60, 140)
    ax2.legend(loc="upper left")

    # Panel 3: Temperature
    ax3.plot(df_pt2["dt"], df_pt2["temperature_c"], color="#2ca02c", linewidth=2.0, label="Body Temp (°C)")
    ax3.axhline(y=38.3, color="orange", linestyle=":", linewidth=1.2, label="Pyrexia (38.3°C)")
    ax3.set_ylabel("Temperature (°C)", fontweight="bold")
    ax3.set_xlabel("Observation Timeline", fontweight="bold")
    ax3.set_ylim(36.0, 39.0)
    ax3.legend(loc="upper left")

    plt.tight_layout()
    plt.savefig("visualizations/activity3_flink_patient_vitals.png", dpi=300)
    plt.close()

    # Chart 2: Alerts by Patient and Ward
    plt.figure(figsize=(10, 5.5))
    sev_cols = [c for c in ["CRITICAL_RED", "URGENT_YELLOW"] if c in alert_counts.columns]
    colors = {"CRITICAL_RED": "#d62728", "URGENT_YELLOW": "#f1c40f"}
    
    plot_df = alert_counts.set_index("patient_name")[sev_cols]
    plot_df.plot(kind="barh", stacked=True, color=[colors[c] for c in sev_cols], figsize=(10, 5.5))
    plt.title("Flink Stream Alert Distribution by Patient & Clinical Severity", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Total Alert Triggers", fontsize=11, fontweight="bold")
    plt.ylabel("Patient", fontsize=11, fontweight="bold")
    plt.legend(title="Severity", loc="lower right")
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("visualizations/activity3_flink_alert_severity.png", dpi=300)
    plt.close()

    # Chart 3: Flink Sliding Window Moving Average vs Raw Stream (PT-03)
    df_pt3_raw = df_raw[df_raw["patient_id"] == "PT-03"].copy()
    df_pt3_raw["dt"] = pd.to_datetime(df_pt3_raw["timestamp"])
    
    df_pt3_win = df_sum[df_sum["patient_id"] == "PT-03"].copy()
    df_pt3_win["dt"] = pd.to_datetime(df_pt3_win["window_end"])

    plt.figure(figsize=(11, 5.5))
    plt.plot(df_pt3_raw["dt"], df_pt3_raw["heart_rate_bpm"], color="#b0bec5", linewidth=1.2, label="Raw Sensor Readings (5s frequency)")
    plt.plot(df_pt3_win["dt"], df_pt3_win["avg_hr"], color="#e74c3c", linewidth=2.8, marker="o", markersize=3, label="Flink 30s Sliding Window Mean (10s slide)")
    plt.axhline(y=125, color="black", linestyle="--", label="Critical Tachycardia Threshold (125 bpm)")
    
    plt.title("Flink Stateful Windowing: Smoothing Sensor Noise via 30s Sliding Windows (PT-03)", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Timeline", fontsize=11, fontweight="bold")
    plt.ylabel("Heart Rate (bpm)", fontsize=11, fontweight="bold")
    plt.legend(loc="upper left")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig("visualizations/activity3_flink_window_stats.png", dpi=300)
    plt.close()

    print("✓ All 3 Flink visualizations generated and saved in visualizations/")
    print("=" * 70)
    print("ACTIVITY 3 COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    run_flink_patient_analytics()

