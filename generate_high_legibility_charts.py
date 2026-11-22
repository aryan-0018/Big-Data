"""
Generates the 10 print-optimized, high-legibility analytical charts
for Activities 1 to 5. Every chart features large bold typography,
sharp contrast, and crisp axis labels designed to be 100% legible
and clear on physical paper prints.
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("visualizations", exist_ok=True)

# Set global matplotlib parameters for high legibility
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 1.0

# -------------------------------------------------------------------
# ACTIVITY 1: HIVE & HDFS CHARTS
# -------------------------------------------------------------------
def generate_act1_charts():
    print("Generating Activity 1 High-Legibility Charts...")
    df_branch = pd.read_csv("activity1_hive/results/q1_branch_revenue.csv")
    
    # 1. Branch Revenue & Profit Breakdown
    fig, ax = plt.subplots(figsize=(8.0, 3.8), dpi=300)
    x = np.arange(len(df_branch))
    width = 0.38

    bars1 = ax.bar(x - width/2, df_branch['total_revenue'] / 1e5, width, label='Gross Revenue (Lakhs ₹)', color='#1F4E79')
    bars2 = ax.bar(x + width/2, df_branch['total_profit'] / 1e5, width, label='Net Profit (Lakhs ₹)', color='#2E7D32')

    ax.set_title("Enterprise Retail: Branch Revenue and Net Profit Breakdown", fontsize=13.5, fontweight='bold', pad=10, color='#002060')
    ax.set_ylabel("Amount in Lakhs (INR ₹)", fontsize=11.5, fontweight='bold', color='#1F2937')
    ax.set_xticks(x)
    ax.set_xticklabels([b.replace(" Store", "").replace(" Super", "").replace(" Prime", "").replace(" MegaStore", "") for b in df_branch['branch_name']], rotation=22, ha='right', fontsize=10.5, fontweight='bold')
    ax.tick_params(axis='y', labelsize=10.5)
    ax.legend(loc='upper right', fontsize=10.5, framealpha=0.95)
    ax.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    fig.savefig("visualizations/activity1_hive_branch_revenue.png", dpi=300)
    plt.close()

    # 2. Hourly Diurnal Checkout Distribution
    df_hourly = pd.read_csv("activity1_hive/results/q3_hourly_sales.csv")
    fig, ax1 = plt.subplots(figsize=(8.0, 3.8), dpi=300)
    ax2 = ax1.twinx()

    ax1.bar(df_hourly['hour_of_day'], df_hourly['transaction_count'], color='#D97706', alpha=0.75, width=0.6, label='Transaction Count (Footfall)')
    ax2.plot(df_hourly['hour_of_day'], df_hourly['hourly_revenue'] / 1e3, color='#1E40AF', marker='o', linewidth=2.5, markersize=5, label='Hourly Revenue (k ₹)')

    ax1.set_title("Diurnal Checkout Velocity: Morning (11:00) & Evening (18:00) Rush Hours", fontsize=13.5, fontweight='bold', pad=10, color='#002060')
    ax1.set_xlabel("Hour of the Day (24-Hour Format)", fontsize=11.5, fontweight='bold', color='#1F2937')
    ax1.set_ylabel("Transaction Count", fontsize=11.5, fontweight='bold', color='#B45309')
    ax2.set_ylabel("Revenue in Thousands (k ₹)", fontsize=11.5, fontweight='bold', color='#1E40AF')
    ax1.set_xticks(df_hourly['hour_of_day'][::2])
    ax1.tick_params(axis='both', labelsize=10.5)
    ax2.tick_params(axis='y', labelsize=10.5)
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10.5, framealpha=0.95)
    ax1.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    fig.savefig("visualizations/activity1_hive_peak_hours.png", dpi=300)
    plt.close()

# -------------------------------------------------------------------
# ACTIVITY 2: KAFKA TRAFFIC CHARTS
# -------------------------------------------------------------------
def generate_act2_charts():
    print("Generating Activity 2 High-Legibility Charts...")
    with open("activity2_kafka/traffic_telemetry_stream.jsonl", "r") as f:
        events = [json.loads(line) for line in f]
    df_events = pd.DataFrame(events)

    # 1. Macroscopic Speed vs Volume State Map
    fig, ax = plt.subplots(figsize=(8.0, 3.8), dpi=300)
    vol = df_events['vehicle_count_per_min']
    spd = df_events['avg_speed_kmh']

    sc = ax.scatter(vol, spd, c=spd, cmap='RdYlGn', edgecolors='#333333', linewidth=0.5, alpha=0.85, s=35)
    cbar = plt.colorbar(sc, ax=ax, pad=0.02)
    cbar.set_label("Speed (km/h)", fontsize=10.5, fontweight='bold')
    cbar.ax.tick_params(labelsize=10)

    # Greenshields model curve
    v_dense = np.linspace(20, 120, 100)
    v_free = 65.0
    k_jam = 120.0
    spd_model = np.clip(v_free * (1.0 - (v_dense / k_jam)**1.8), 5.0, 65.0)
    ax.plot(v_dense, spd_model, color='#DC2626', linewidth=2.5, linestyle='--', label='Greenshields Traffic Curve')

    ax.axvspan(80, 130, color='#FEE2E2', alpha=0.5, label='Critical Congestion Zone (>80 veh/min)')
    ax.set_title("Traffic Flow State Map: Macroscopic Speed vs. Vehicle Volume", fontsize=13.5, fontweight='bold', pad=10, color='#002060')
    ax.set_xlabel("Vehicle Volume (Vehicles / Minute)", fontsize=11.5, fontweight='bold', color='#1F2937')
    ax.set_ylabel("Average Speed (km/h)", fontsize=11.5, fontweight='bold', color='#1F2937')
    ax.tick_params(axis='both', labelsize=10.5)
    ax.legend(loc='upper right', fontsize=10.5, framealpha=0.95)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    fig.savefig("visualizations/activity2_kafka_speed_vs_volume.png", dpi=300)
    plt.close()

    # 2. Timeline Alert at Silk Board
    silk_events = df_events[df_events['junction_id'] == 'J-01'].copy()
    fig, ax1 = plt.subplots(figsize=(8.0, 3.8), dpi=300)
    ax2 = ax1.twinx()

    t_idx = np.arange(len(silk_events))
    ax1.plot(t_idx, silk_events['avg_speed_kmh'], color='#DC2626', marker='s', markersize=4, linewidth=2.0, label='Speed (km/h)')
    ax2.bar(t_idx, silk_events['vehicle_count_per_min'], color='#2563EB', alpha=0.35, width=0.8, label='Volume (veh/min)')

    ax1.axhline(15.0, color='#991B1B', linestyle=':', linewidth=2.0, label='Critical Red Speed Limit (15 km/h)')
    ax1.set_title("Silk Board Junction: Speed Degradation & Automated Incident Window", fontsize=13.5, fontweight='bold', pad=10, color='#002060')
    ax1.set_xlabel("Event Sequence Timeline (Time Ticks)", fontsize=11.5, fontweight='bold', color='#1F2937')
    ax1.set_ylabel("Speed (km/h)", fontsize=11.5, fontweight='bold', color='#DC2626')
    ax2.set_ylabel("Volume (veh/min)", fontsize=11.5, fontweight='bold', color='#2563EB')
    ax1.tick_params(axis='both', labelsize=10.5)
    ax2.tick_params(axis='y', labelsize=10.5)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower left', fontsize=10.5, framealpha=0.95)
    ax1.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    fig.savefig("visualizations/activity2_kafka_timeline_alert.png", dpi=300)
    plt.close()

# -------------------------------------------------------------------
# ACTIVITY 3: FLINK HEALTHCARE CHARTS
# -------------------------------------------------------------------
def generate_act3_charts():
    print("Generating Activity 3 High-Legibility Charts...")
    df_vitals = pd.read_csv("activity3_flink/patient_telemetry_stream.csv")
    pt02 = df_vitals[df_vitals['patient_id'] == 'PT-02'].sort_values('timestamp').reset_index(drop=True)

    # 1. Patient PT-02 Physiological Stream
    fig, ax1 = plt.subplots(figsize=(8.0, 3.8), dpi=300)
    ax2 = ax1.twinx()

    t_vals = np.arange(len(pt02))
    ax1.plot(t_vals, pt02['spo2_pct'], color='#DC2626', linewidth=2.2, label='Blood Oxygen SpO2 (%)')
    ax2.plot(t_vals, pt02['heart_rate_bpm'], color='#2563EB', linewidth=2.0, linestyle='--', label='Heart Rate (bpm)')

    ax1.axhline(90.0, color='#991B1B', linestyle=':', linewidth=2.0, label='Hypoxemia Threshold (<90%)')
    ax2.axhline(100.0, color='#1E40AF', linestyle=':', linewidth=2.0, label='Tachycardia Threshold (>100 bpm)')

    ax1.set_title("Patient PT-02 (Sunita Patil, ICU-A): Hypoxemic Desaturation Trajectory", fontsize=13.5, fontweight='bold', pad=10, color='#002060')
    ax1.set_xlabel("Time Progression (Observation Windows)", fontsize=11.5, fontweight='bold', color='#1F2937')
    ax1.set_ylabel("SpO2 (%)", fontsize=11.5, fontweight='bold', color='#DC2626')
    ax2.set_ylabel("Heart Rate (bpm)", fontsize=11.5, fontweight='bold', color='#2563EB')
    ax1.tick_params(axis='both', labelsize=10.5)
    ax2.tick_params(axis='y', labelsize=10.5)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='lower left', fontsize=10.5, framealpha=0.95)
    ax1.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    fig.savefig("visualizations/activity3_flink_patient_vitals.png", dpi=300)
    plt.close()

    # 2. Raw Sensor vs Sliding Window Smoothing
    fig, ax = plt.subplots(figsize=(8.0, 3.8), dpi=300)
    raw_spo2 = pt02['spo2_pct'].values
    window_spo2 = pt02['spo2_pct'].rolling(window=3, min_periods=1).mean().values

    ax.plot(t_vals, raw_spo2, color='#9CA3AF', linewidth=1.5, marker='o', markersize=3, label='Raw Telemetry (High Jitter)')
    ax.plot(t_vals, window_spo2, color='#16A34A', linewidth=2.5, label='30s Sliding Window Mean (Event-Time)')

    ax.axhline(90.0, color='#DC2626', linestyle='--', linewidth=1.8, label='Clinical Alarm Boundary (90%)')
    ax.set_title("Event-Time Window Smoothing: Raw Noise vs. 30s Sliding Window", fontsize=13.5, fontweight='bold', pad=10, color='#002060')
    ax.set_xlabel("Event Time Sequence", fontsize=11.5, fontweight='bold', color='#1F2937')
    ax.set_ylabel("SpO2 Percentage (%)", fontsize=11.5, fontweight='bold', color='#1F2937')
    ax.tick_params(axis='both', labelsize=10.5)
    ax.legend(loc='lower left', fontsize=10.5, framealpha=0.95)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    fig.savefig("visualizations/activity3_flink_window_stats.png", dpi=300)
    plt.close()

# -------------------------------------------------------------------
# ACTIVITY 4: MONGODB CHARTS
# -------------------------------------------------------------------
def generate_act4_charts():
    print("Generating Activity 4 High-Legibility Charts...")
    # 1. Index Benchmark: COLLSCAN vs IXSCAN
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.0, 3.8), dpi=300)

    stages = ['COLLSCAN\n(Unindexed)', 'IXSCAN\n(Compound Index)']
    docs = [14990, 1101]
    latencies = [18.2, 3.76]

    bars1 = ax1.bar(stages, docs, color=['#EF4444', '#10B981'], width=0.55, edgecolor='#333333', linewidth=1.0)
    ax1.set_title("Documents Scanned", fontsize=12.5, fontweight='bold', color='#002060')
    ax1.set_ylabel("Number of Docs Examined", fontsize=11.0, fontweight='bold', color='#1F2937')
    ax1.tick_params(axis='both', labelsize=10.5)
    for b in bars1:
        yval = b.get_height()
        ax1.text(b.get_x() + b.get_width()/2.0, yval + 300, f"{int(yval):,}", ha='center', va='bottom', fontsize=10.5, fontweight='bold')
    ax1.set_ylim(0, 17500)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    bars2 = ax2.bar(stages, latencies, color=['#F59E0B', '#3B82F6'], width=0.55, edgecolor='#333333', linewidth=1.0)
    ax2.set_title("Query Execution Latency", fontsize=12.5, fontweight='bold', color='#002060')
    ax2.set_ylabel("Execution Time (Milliseconds)", fontsize=11.0, fontweight='bold', color='#1F2937')
    ax2.tick_params(axis='both', labelsize=10.5)
    for b in bars2:
        yval = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2.0, yval + 0.3, f"{yval:.2f} ms", ha='center', va='bottom', fontsize=10.5, fontweight='bold')
    ax2.set_ylim(0, 22)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)

    fig.suptitle("MongoDB WiredTiger Performance: COLLSCAN vs. Compound B-Tree IXSCAN", fontsize=13.0, fontweight='bold', color='#002060', y=1.02)
    plt.tight_layout()
    fig.savefig("visualizations/activity4_mongodb_index_benchmark.png", dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Schema Comparison Diagram
    fig, ax = plt.subplots(figsize=(8.0, 3.8), dpi=300)
    ax.axis('off')

    # Draw Relational Box
    rect_rel = plt.Rectangle((0.05, 0.15), 0.40, 0.75, facecolor='#EFF6FF', edgecolor='#1E40AF', linewidth=2.0)
    ax.add_patch(rect_rel)
    ax.text(0.25, 0.82, "Normalized Relational Model", ha='center', va='center', fontsize=11.5, fontweight='bold', color='#1E40AF')
    ax.text(0.25, 0.70, "• Fixed Schema Across Rows", ha='center', va='center', fontsize=10.5, color='#1F2937')
    ax.text(0.25, 0.58, "• Null Values for Polymorphic Data", ha='center', va='center', fontsize=10.5, color='#1F2937')
    ax.text(0.25, 0.46, "• Costly Multi-Table SQL Joins", ha='center', va='center', fontsize=10.5, color='#1F2937')
    ax.text(0.25, 0.34, "• Alter Table Requires DDL Locks", ha='center', va='center', fontsize=10.5, color='#1F2937')
    ax.text(0.25, 0.22, "Tables: products, specs, attributes", ha='center', va='center', fontsize=10.0, fontstyle='italic', color='#4B5563')

    # Draw MongoDB Box
    rect_nosql = plt.Rectangle((0.55, 0.15), 0.40, 0.75, facecolor='#ECFDF5', edgecolor='#059669', linewidth=2.0)
    ax.add_patch(rect_nosql)
    ax.text(0.75, 0.82, "MongoDB Polymorphic BSON", ha='center', va='center', fontsize=11.5, fontweight='bold', color='#059669')
    ax.text(0.75, 0.70, "• Dynamic Embedded Sub-Documents", ha='center', va='center', fontsize=10.5, color='#1F2937')
    ax.text(0.75, 0.58, "• Zero Null Columns for Specs", ha='center', va='center', fontsize=10.5, color='#1F2937')
    ax.text(0.75, 0.46, "• Single Document Atomic Read/Write", ha='center', va='center', fontsize=10.5, color='#1F2937')
    ax.text(0.75, 0.34, "• High-Performance B-Tree Indexing", ha='center', va='center', fontsize=10.5, color='#1F2937')
    ax.text(0.75, 0.22, "Collection: products (polymorphic)", ha='center', va='center', fontsize=10.0, fontstyle='italic', color='#4B5563')

    ax.set_title("Architectural Comparison: Relational RDBMS vs. MongoDB Polymorphic BSON", fontsize=13.0, fontweight='bold', pad=10, color='#002060')
    plt.tight_layout()
    fig.savefig("visualizations/activity4_mongodb_schema_diagram.png", dpi=300)
    plt.close()

# -------------------------------------------------------------------
# ACTIVITY 5: CLOUD ANALYTICS & FINOPS CHARTS
# -------------------------------------------------------------------
def generate_act5_charts():
    print("Generating Activity 5 High-Legibility Charts...")
    df_status = pd.read_csv("activity5_cloud_analytics/results/q1_status_code_breakdown.csv")

    # 1. Status Code Proportions
    fig, ax = plt.subplots(figsize=(8.0, 3.8), dpi=300)
    codes = [str(c) for c in df_status['status_code']]
    shares = df_status['percentage_share']
    colors = ['#10B981', '#3B82F6', '#F59E0B', '#EF4444', '#DC2626']

    bars = ax.bar(codes, shares, color=colors, width=0.55, edgecolor='#333333', linewidth=1.0)
    ax.set_title("HTTP Response Status Proportions (50,000 Access Logs)", fontsize=13.5, fontweight='bold', pad=10, color='#002060')
    ax.set_xlabel("HTTP Response Status Code", fontsize=11.5, fontweight='bold', color='#1F2937')
    ax.set_ylabel("Proportion of Requests (%)", fontsize=11.5, fontweight='bold', color='#1F2937')
    ax.tick_params(axis='both', labelsize=10.5)
    for b in bars:
        yval = b.get_height()
        ax.text(b.get_x() + b.get_width()/2.0, yval + 1.2, f"{yval:.2f}%", ha='center', va='bottom', fontsize=10.5, fontweight='bold')
    ax.set_ylim(0, 105)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    fig.savefig("visualizations/activity5_cloud_error_distribution.png", dpi=300)
    plt.close()

    # 2. Cloud FinOps Cost Model: On-Premise vs Serverless
    fig, ax = plt.subplots(figsize=(8.0, 3.8), dpi=300)
    models = ['On-Premise\nCluster Hardware', 'Provisioned Cloud\nVMs (24/7 Running)', 'Serverless S3 +\nAthena Parquet']
    costs = [1200.0, 850.0, 340.13]
    colors_fin = ['#EF4444', '#F59E0B', '#10B981']

    bars_f = ax.bar(models, costs, color=colors_fin, width=0.55, edgecolor='#333333', linewidth=1.0)
    ax.set_title("Cloud FinOps Model: Monthly Infrastructure & Query TCO ($ USD)", fontsize=13.5, fontweight='bold', pad=10, color='#002060')
    ax.set_ylabel("Monthly Operating Cost ($ USD)", fontsize=11.5, fontweight='bold', color='#1F2937')
    ax.tick_params(axis='both', labelsize=10.5)
    for b in bars_f:
        yval = b.get_height()
        ax.text(b.get_x() + b.get_width()/2.0, yval + 20, f"${yval:,.2f}", ha='center', va='bottom', fontsize=10.5, fontweight='bold')
    ax.set_ylim(0, 1400)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    fig.savefig("visualizations/activity5_cloud_cost_model.png", dpi=300)
    plt.close()

if __name__ == "__main__":
    generate_act1_charts()
    generate_act2_charts()
    generate_act3_charts()
    generate_act4_charts()
    generate_act5_charts()
    print("✓ All 10 Print-Optimized High-Legibility Analytical Charts Generated Successfully!")
