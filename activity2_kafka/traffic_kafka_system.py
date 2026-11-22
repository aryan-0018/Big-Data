"""
Smart City Traffic Ingestion & Congestion Alert Engine using Apache Kafka Architecture.
Simulates multi-partition Kafka topics, real-time producers, consumer groups, 
and automated threshold-based traffic congestion alert generation.
"""

import os
import json
import time
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 11})

os.makedirs("activity2_kafka", exist_ok=True)
os.makedirs("visualizations", exist_ok=True)

# ---------------------------------------------------------------------
# KAFKA CORE ARCHITECTURE SIMULATOR (BROKER, TOPIC, PARTITIONS)
# ---------------------------------------------------------------------
class KafkaBroker:
    """Simulates an Apache Kafka Broker managing topic partitions and consumer offsets."""
    def __init__(self, broker_id="broker-1"):
        self.broker_id = broker_id
        self.topics = {}
        self.consumer_offsets = {}  # {group_id: {topic: {partition: offset}}}

    def create_topic(self, topic_name, num_partitions=3):
        if topic_name not in self.topics:
            self.topics[topic_name] = [[] for _ in range(num_partitions)]
            print(f"[Broker {self.broker_id}] Created Topic: '{topic_name}' with {num_partitions} partitions.")

    def publish(self, topic_name, key, value):
        if topic_name not in self.topics:
            self.create_topic(topic_name)
        partitions = self.topics[topic_name]
        # Partition selection via MurmurHash-like hashing of key
        partition_id = hash(key) % len(partitions)
        offset = len(partitions[partition_id])
        record = {
            "topic": topic_name,
            "partition": partition_id,
            "offset": offset,
            "key": key,
            "value": value,
            "published_at": datetime.now().isoformat()
        }
        partitions[partition_id].append(record)
        return partition_id, offset

    def consume(self, topic_name, group_id, max_records=100):
        if topic_name not in self.topics:
            return []
        
        if group_id not in self.consumer_offsets:
            self.consumer_offsets[group_id] = {}
        if topic_name not in self.consumer_offsets[group_id]:
            self.consumer_offsets[group_id][topic_name] = {p: 0 for p in range(len(self.topics[topic_name]))}

        records = []
        for p_id, partition in enumerate(self.topics[topic_name]):
            current_offset = self.consumer_offsets[group_id][topic_name][p_id]
            while current_offset < len(partition) and len(records) < max_records:
                records.append(partition[current_offset])
                current_offset += 1
            self.consumer_offsets[group_id][topic_name][p_id] = current_offset

        return records

# ---------------------------------------------------------------------
# SENSOR DATA & TOPOLOGY
# ---------------------------------------------------------------------
JUNCTIONS = [
    {"junction_id": "J-01", "name": "Silk Board Junction", "city": "Bengaluru", "corridor": "Outer Ring Road", "capacity_vpm": 100},
    {"junction_id": "J-02", "name": "Hebbal Flyover", "city": "Bengaluru", "corridor": "Airport Expressway", "capacity_vpm": 95},
    {"junction_id": "J-03", "name": "Marathahalli Bridge", "city": "Bengaluru", "corridor": "IT Corridor", "capacity_vpm": 90},
    {"junction_id": "J-04", "name": "BKC Connector", "city": "Mumbai", "corridor": "Financial District Link", "capacity_vpm": 110},
    {"junction_id": "J-05", "name": "Western Express Highway - Andheri", "city": "Mumbai", "corridor": "WEH Arterial", "capacity_vpm": 120},
    {"junction_id": "J-06", "name": "Connaught Place Radial 3", "city": "Delhi", "corridor": "Central Circle", "capacity_vpm": 85},
    {"junction_id": "J-07", "name": "Dhaula Kuan Underpass", "city": "Delhi", "corridor": "Ring Road Arterial", "capacity_vpm": 105},
    {"junction_id": "J-08", "name": "Gachibowli Junction", "city": "Hyderabad", "corridor": "Cyberabad Hub", "capacity_vpm": 95}
]

def run_kafka_traffic_simulation():
    print("=" * 70)
    print("STARTING ACTIVITY 2: APACHE KAFKA SMART CITY TRAFFIC INGESTION & ALERT SYSTEM")
    print("=" * 70)

    broker = KafkaBroker(broker_id="kafka-node-101")
    telemetry_topic = "smartcity-traffic-telemetry"
    alerts_topic = "traffic-congestion-alerts"

    broker.create_topic(telemetry_topic, num_partitions=4)
    broker.create_topic(alerts_topic, num_partitions=2)

    # -----------------------------------------------------------------
    # STEP 1: PRODUCER SIMULATION (TELEMETRY STREAM GENERATION)
    # -----------------------------------------------------------------
    print("\n[Kafka Producer] Publishing high-velocity traffic sensor telemetry...")
    random.seed(101)
    np.random.seed(101)

    all_telemetry = []
    base_time = datetime(2025, 11, 10, 7, 0, 0) # 7:00 AM to 11:00 AM (Morning rush)
    num_intervals = 120 # Every 2 minutes = 4 hours of monitoring

    for step in range(num_intervals):
        cur_time = base_time + timedelta(minutes=step * 2)
        hour = cur_time.hour
        
        for j in JUNCTIONS:
            # Baseline dynamics with rush hour peak (8:30 - 10:00)
            is_rush = (8 <= hour <= 9) or (hour == 10 and cur_time.minute <= 15)
            
            # Special traffic bottleneck event at Silk Board & BKC
            has_incident = (j["junction_id"] in ["J-01", "J-04"]) and (8 <= hour <= 9 and 15 <= cur_time.minute <= 50)
            
            if has_incident:
                # Heavy bottleneck / gridlock
                vehicle_count = random.randint(88, 125)
                avg_speed = round(random.uniform(5.0, 16.0), 1)
                occupancy = round(random.uniform(85.0, 99.5), 1)
            elif is_rush:
                vehicle_count = random.randint(65, 95)
                avg_speed = round(random.uniform(18.0, 32.0), 1)
                occupancy = round(random.uniform(65.0, 85.0), 1)
            else:
                vehicle_count = random.randint(25, 55)
                avg_speed = round(random.uniform(42.0, 68.0), 1)
                occupancy = round(random.uniform(25.0, 50.0), 1)

            payload = {
                "sensor_id": f"SNSR-{j['junction_id']}",
                "junction_id": j["junction_id"],
                "junction_name": j["name"],
                "city": j["city"],
                "corridor": j["corridor"],
                "timestamp": cur_time.strftime("%Y-%m-%d %H:%M:%S"),
                "vehicle_count_per_min": vehicle_count,
                "avg_speed_kmh": avg_speed,
                "occupancy_pct": occupancy,
                "weather": "Clear"
            }
            
            # Kafka Producer publishes message keyed by junction_id (guarantees partition ordering)
            part, off = broker.publish(telemetry_topic, key=j["junction_id"], value=payload)
            all_telemetry.append(payload)

    print(f"✓ Producer successfully published {len(all_telemetry):,} telemetry records to '{telemetry_topic}'.")

    # Save telemetry stream to JSON Lines
    with open("activity2_kafka/traffic_telemetry_stream.jsonl", "w", encoding="utf-8") as f:
        for item in all_telemetry:
            f.write(json.dumps(item) + "\n")

    # -----------------------------------------------------------------
    # STEP 2: CONSUMER APPLICATION & REAL-TIME CONGESTION DETECTION
    # -----------------------------------------------------------------
    print("\n[Kafka Consumer Group: 'traffic-ops-engine'] Ingesting and evaluating stream...")
    
    consumed_records = broker.consume(telemetry_topic, group_id="traffic-ops-engine", max_records=len(all_telemetry))
    print(f"✓ Consumer group retrieved {len(consumed_records):,} records across all partitions.")

    generated_alerts = []
    
    # Congestion thresholds
    # CRITICAL: Speed <= 15 km/h AND Vehicle count >= 80 veh/min (Gridlock)
    # MAJOR: Speed <= 28 km/h AND Vehicle count >= 65 veh/min (Heavy Congestion)
    # MODERATE: Speed <= 38 km/h AND Vehicle count >= 55 veh/min (Approaching Capacity)

    for record in consumed_records:
        msg = record["value"]
        speed = msg["avg_speed_kmh"]
        v_count = msg["vehicle_count_per_min"]
        
        severity = None
        action_plan = None

        if speed <= 15.0 and v_count >= 80:
            severity = "CRITICAL_RED"
            action_plan = "Emergency Intervention: Extend green signal by +45s; Trigger VMS diversion; Dispatch traffic warden."
        elif speed <= 28.0 and v_count >= 65:
            severity = "MAJOR_AMBER"
            action_plan = "Dynamic Signal Timing: Extend green phase by +25s; Advise secondary bypass corridor."
        elif speed <= 38.0 and v_count >= 55:
            severity = "MODERATE_YELLOW"
            action_plan = "Monitoring Alert: Signal optimization active; Notify navigation map providers."

        if severity:
            alert = {
                "alert_id": f"ALT-{msg['junction_id']}-{record['offset']}",
                "timestamp": msg["timestamp"],
                "junction_id": msg["junction_id"],
                "junction_name": msg["junction_name"],
                "city": msg["city"],
                "corridor": msg["corridor"],
                "severity": severity,
                "detected_speed_kmh": speed,
                "vehicle_count_per_min": v_count,
                "occupancy_pct": msg["occupancy_pct"],
                "mitigation_action": action_plan
            }
            # Publish alert back to Kafka alerts topic
            broker.publish(alerts_topic, key=msg["junction_id"], value=alert)
            generated_alerts.append(alert)

    print(f"✓ Identified and published {len(generated_alerts)} congestion alerts to '{alerts_topic}'.")

    # Save alerts to JSON
    with open("activity2_kafka/traffic_congestion_alerts.json", "w", encoding="utf-8") as f:
        json.dump(generated_alerts, f, indent=2)

    # -----------------------------------------------------------------
    # STEP 3: ANALYTICAL SUMMARY & INCIDENT STATISTICS
    # -----------------------------------------------------------------
    df_alerts = pd.DataFrame(generated_alerts)
    df_telemetry = pd.DataFrame(all_telemetry)

    summary = df_alerts.groupby(["junction_id", "junction_name", "city", "severity"]).size().unstack(fill_value=0)
    summary["TOTAL_ALERTS"] = summary.sum(axis=1)
    summary = summary.sort_values("TOTAL_ALERTS", ascending=False).reset_index()
    summary.to_csv("activity2_kafka/junction_congestion_summary.csv", index=False)
    
    print("\n[Junction Congestion Alert Summary Table]")
    print(summary.to_string())

    # -----------------------------------------------------------------
    # STEP 4: VISUALIZATION GENERATION
    # -----------------------------------------------------------------
    print("\nGenerating Kafka traffic analytics charts...")

    # Chart 1: Speed vs Volume Scatter & Congestion Threshold Boundaries
    plt.figure(figsize=(10, 6.5))
    scatter = plt.scatter(
        df_telemetry["vehicle_count_per_min"],
        df_telemetry["avg_speed_kmh"],
        c=df_telemetry["occupancy_pct"],
        cmap="viridis_r",
        alpha=0.65,
        edgecolors="none",
        s=35
    )
    cbar = plt.colorbar(scatter)
    cbar.set_label("Road Occupancy (%)", fontsize=11, fontweight="bold")
    
    # Overlay threshold boundaries
    plt.axvline(x=80, color="red", linestyle="--", linewidth=1.5, label="Critical Volume Threshold (80 veh/min)")
    plt.axhline(y=15, color="red", linestyle="--", linewidth=1.5, label="Critical Speed Floor (15 km/h)")
    plt.fill_between([80, 130], 0, 15, color="red", alpha=0.18, label="CRITICAL GRIDLOCK ZONE")
    plt.fill_between([65, 130], 15, 28, color="orange", alpha=0.15, label="HEAVY CONGESTION ZONE")

    plt.title("Smart City Traffic Sensor Stream: Speed vs. Vehicle Volume State Map", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Vehicle Count (Vehicles / Minute)", fontsize=11, fontweight="bold")
    plt.ylabel("Average Vehicle Speed (km/h)", fontsize=11, fontweight="bold")
    plt.xlim(20, 130)
    plt.ylim(0, 75)
    plt.legend(loc="upper right", frameon=True)
    plt.tight_layout()
    plt.savefig("visualizations/activity2_kafka_speed_vs_volume.png", dpi=300)
    plt.close()

    # Chart 2: Congestion Alerts by Junction and Severity
    plt.figure(figsize=(11, 5.5))
    severity_cols = [c for c in ["CRITICAL_RED", "MAJOR_AMBER", "MODERATE_YELLOW"] if c in summary.columns]
    colors = {"CRITICAL_RED": "#d62728", "MAJOR_AMBER": "#ff7f0e", "MODERATE_YELLOW": "#bcbd22"}
    
    summary_plot = summary.set_index("junction_name")[severity_cols]
    summary_plot.plot(kind="barh", stacked=True, color=[colors[c] for c in severity_cols], figsize=(11, 5.5))
    plt.title("Kafka Traffic Stream: Alert Distribution Across Monitored Urban Junctions", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("Number of Automated Operator Alerts", fontsize=11, fontweight="bold")
    plt.ylabel("Junction Name", fontsize=11, fontweight="bold")
    plt.legend(title="Alert Severity", loc="lower right")
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("visualizations/activity2_kafka_junction_severity.png", dpi=300)
    plt.close()

    # Chart 3: Real-Time Incident Timeline for Silk Board Junction (J-01)
    df_j01 = df_telemetry[df_telemetry["junction_id"] == "J-01"].copy()
    df_j01["dt"] = pd.to_datetime(df_j01["timestamp"])
    
    fig, ax1 = plt.subplots(figsize=(12, 5.5))
    ax2 = ax1.twinx()
    
    ax1.plot(df_j01["dt"], df_j01["avg_speed_kmh"], color="#1f77b4", linewidth=2.5, marker="o", markersize=3, label="Avg Speed (km/h)")
    ax2.plot(df_j01["dt"], df_j01["vehicle_count_per_min"], color="#d62728", linewidth=2.0, linestyle="--", label="Vehicle Count (veh/min)")
    
    ax1.axhline(y=15, color="red", linestyle=":", label="Critical Speed Floor (15 km/h)")
    
    # Highlight alert period
    alerts_j01 = [a for a in generated_alerts if a["junction_id"] == "J-01"]
    if alerts_j01:
        alert_times = [pd.to_datetime(a["timestamp"]) for a in alerts_j01 if a["severity"] == "CRITICAL_RED"]
        if alert_times:
            ax1.axvspan(min(alert_times), max(alert_times), color="red", alpha=0.15, label="Kafka CRITICAL_RED Alert Trigger Window")

    ax1.set_xlabel("Timeline (Morning Peak Observation Window)", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Speed (km/h)", color="#1f77b4", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Vehicle Count (veh/min)", color="#d62728", fontsize=11, fontweight="bold")
    plt.title("Real-Time Telemetry & Kafka Alert Window: Silk Board Junction (J-01)", fontsize=13, fontweight="bold", pad=12)
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="lower left")
    ax1.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("visualizations/activity2_kafka_timeline_alert.png", dpi=300)
    plt.close()

    print("✓ All 3 Kafka visualizations generated and saved in visualizations/")
    print("=" * 70)
    print("ACTIVITY 2 COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    run_kafka_traffic_simulation()

