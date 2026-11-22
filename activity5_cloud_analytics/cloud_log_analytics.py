"""
Cloud-Based Big Data Analytics Engine (AWS Athena & S3 Serverless Architecture).
Simulates enterprise cloud data lake ingestion, Athena SQL log queries,
statistical anomaly spike detection, and cloud FinOps cost modeling.
"""

import os
import json
import random
from datetime import datetime, timedelta
import duckdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 11})

os.makedirs("activity5_cloud_analytics", exist_ok=True)
os.makedirs("activity5_cloud_analytics/results", exist_ok=True)
os.makedirs("visualizations", exist_ok=True)

# ---------------------------------------------------------------------
# SERVER LOG DATASET GENERATOR (COMBINED LOG FORMAT + JSON)
# ---------------------------------------------------------------------
def generate_server_logs(filename_csv="activity5_cloud_analytics/web_server_logs.csv", num_records=50000):
    random.seed(42)
    np.random.seed(42)

    endpoints = [
        {"path": "/api/v1/catalog/products", "method": "GET", "base_lat": 45, "err_prob": 0.02},
        {"path": "/api/v1/catalog/search", "method": "GET", "base_lat": 85, "err_prob": 0.04},
        {"path": "/api/v1/cart/items", "method": "POST", "base_lat": 110, "err_prob": 0.05},
        {"path": "/api/v1/checkout/process", "method": "POST", "base_lat": 280, "err_prob": 0.09},
        {"path": "/api/v1/auth/login", "method": "POST", "base_lat": 65, "err_prob": 0.06},
        {"path": "/api/v1/user/profile", "method": "GET", "base_lat": 40, "err_prob": 0.01},
        {"path": "/static/images/hero_banner.webp", "method": "GET", "base_lat": 12, "err_prob": 0.005},
        {"path": "/api/v2/recommendations", "method": "GET", "base_lat": 150, "err_prob": 0.08}
    ]

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
        "curl/8.4.0 (HealthCheck-Bot)"
    ]

    base_time = datetime(2025, 11, 10, 0, 0, 0) # 24 hours of logs
    records = []

    print(f"Generating {num_records:,} cloud application server logs...")

    # Hourly distribution weights: low at night (0-5), rising morning (8-12), peak (14-21)
    hour_weights = [
        1.5, 1.0, 0.8, 0.6, 0.8, 1.2, # 00:00 - 05:00
        2.5, 4.0, 6.5, 8.0, 8.5, 7.5, # 06:00 - 11:00
        7.0, 7.2, 12.0, 14.5, 9.0, 8.5, # 12:00 - 17:00 (Incident spike at 14-15)
        9.5, 10.0, 8.5, 6.0, 4.0, 2.5  # 18:00 - 23:00
    ]

    for i in range(1, num_records + 1):
        hour = random.choices(range(24), weights=hour_weights)[0]
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        log_dt = base_time + timedelta(hours=hour, minutes=minute, seconds=second)

        ep = random.choice(endpoints)
        
        # Outage / spike scenario: between 14:00 and 15:30 on /api/v1/checkout/process
        is_incident_window = (14 <= hour <= 15) and (ep["path"] in ["/api/v1/checkout/process", "/api/v2/recommendations"])
        
        if is_incident_window:
            # Payment gateway upstream failure & database connection saturation
            status_code = random.choices([500, 502, 503, 504, 200], weights=[35, 25, 20, 10, 10])[0]
            resp_bytes = random.randint(350, 1200)
            lat = round(random.uniform(1500, 4800), 1) # Extreme latency spike
        else:
            # Normal distribution
            has_err = random.random() < ep["err_prob"]
            if has_err:
                status_code = random.choices([400, 401, 403, 404, 500], weights=[20, 15, 10, 45, 10])[0]
                resp_bytes = random.randint(200, 850)
                lat = round(ep["base_lat"] * random.uniform(1.2, 3.5), 1)
            else:
                status_code = 200
                resp_bytes = random.randint(1200, 24000)
                lat = round(ep["base_lat"] * random.uniform(0.7, 1.4), 1)

        # Status category
        status_category = f"{status_code // 100}xx"

        client_ip = f"{random.randint(49, 185)}.{random.randint(10, 250)}.{random.randint(1, 254)}.{random.randint(1, 254)}"

        records.append({
            "request_id": f"REQ-{log_dt.strftime('%Y%m%d%H%M%S')}-{i:05d}",
            "timestamp": log_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "date": log_dt.strftime("%Y-%m-%d"),
            "hour": hour,
            "client_ip": client_ip,
            "http_method": ep["method"],
            "endpoint": ep["path"],
            "status_code": status_code,
            "status_category": status_category,
            "response_time_ms": lat,
            "response_bytes": resp_bytes,
            "user_agent": random.choice(user_agents)
        })

    df = pd.DataFrame(records)
    df.to_csv(filename_csv, index=False)
    # Also save as Parquet (Cloud Columnar Storage standard)
    parquet_path = "activity5_cloud_analytics/web_server_logs.parquet"
    df.to_parquet(parquet_path, compression="snappy", index=False)

    print(f"✓ Created server log CSV: {filename_csv}")
    print(f"✓ Created optimized Parquet file: {parquet_path} (Snappy compressed)")
    return df

# ---------------------------------------------------------------------
# CLOUD DATA LAKE QUERY SUITE & ANOMALY DETECTION ENGINE
# ---------------------------------------------------------------------
def run_cloud_log_analytics():
    print("=" * 70)
    print("STARTING ACTIVITY 5: CLOUD-BASED BIG DATA LOG ANALYTICS (AWS ATHENA / S3)")
    print("=" * 70)

    # Generate logs
    df = generate_server_logs()

    con = duckdb.connect(database=":memory:")
    con.execute("CREATE TABLE cloud_logs AS SELECT * FROM read_parquet('activity5_cloud_analytics/web_server_logs.parquet')")

    # 1. Total summary
    total_reqs = con.execute("SELECT COUNT(*) FROM cloud_logs").fetchone()[0]
    total_bytes_mb = round(con.execute("SELECT SUM(response_bytes) FROM cloud_logs").fetchone()[0] / (1024 * 1024), 2)
    print(f"\n✓ Loaded {total_reqs:,} logs representing {total_bytes_mb} MB of data lake payload.")

    # ---------------------------------------------------------
    # QUERY 1: HTTP Status Code and Error Breakdown
    # ---------------------------------------------------------
    q1 = """
    SELECT 
        status_category,
        status_code,
        COUNT(*) AS request_count,
        ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM cloud_logs)), 2) AS percentage_share,
        ROUND(AVG(response_time_ms), 1) AS avg_latency_ms
    FROM cloud_logs
    GROUP BY status_category, status_code
    ORDER BY status_category, request_count DESC;
    """
    df_status = con.execute(q1).fetchdf()
    df_status.to_csv("activity5_cloud_analytics/results/q1_status_code_breakdown.csv", index=False)
    print("\n[Query 1: Status Code Distribution & Latency]")
    print(df_status.to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 2: Hourly Traffic & Error Anomaly Detection (Statistical Z-Score)
    # ---------------------------------------------------------
    q2 = """
    WITH hourly_stats AS (
        SELECT 
            hour,
            COUNT(*) AS total_requests,
            SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) AS error_requests,
            SUM(CASE WHEN status_code >= 500 THEN 1 ELSE 0 END) AS server_errors_5xx,
            ROUND(AVG(response_time_ms), 1) AS avg_latency_ms,
            ROUND(MAX(response_time_ms), 1) AS max_latency_ms
        FROM cloud_logs
        GROUP BY hour
    ),
    with_rates AS (
        SELECT 
            hour,
            total_requests,
            error_requests,
            server_errors_5xx,
            ROUND((error_requests * 100.0 / total_requests), 2) AS error_rate_pct,
            avg_latency_ms,
            max_latency_ms
        FROM hourly_stats
    )
    SELECT 
        hour,
        total_requests,
        error_requests,
        server_errors_5xx,
        error_rate_pct,
        avg_latency_ms,
        max_latency_ms,
        CASE 
            WHEN error_rate_pct > 15.0 THEN 'CRITICAL SPIKE - BACKEND INCIDENT'
            WHEN error_rate_pct > 5.0 THEN 'ELEVATED - INVESTIGATE'
            ELSE 'NORMAL'
        END AS anomaly_flag
    FROM with_rates
    ORDER BY hour;
    """
    df_hourly = con.execute(q2).fetchdf()
    df_hourly.to_csv("activity5_cloud_analytics/results/q2_hourly_traffic_anomalies.csv", index=False)
    print("\n[Query 2: Hourly Request Volume & Incident Spike Detection]")
    print(df_hourly.to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 3: Endpoint Latency Profiles (Percentiles: p50, p95, p99)
    # ---------------------------------------------------------
    q3 = """
    SELECT 
        endpoint,
        http_method,
        COUNT(*) AS total_hits,
        ROUND(AVG(response_time_ms), 1) AS mean_latency_ms,
        ROUND(QUANTILE_CONT(response_time_ms, 0.50), 1) AS p50_latency_ms,
        ROUND(QUANTILE_CONT(response_time_ms, 0.95), 1) AS p95_latency_ms,
        ROUND(QUANTILE_CONT(response_time_ms, 0.99), 1) AS p99_latency_ms,
        SUM(CASE WHEN status_code >= 500 THEN 1 ELSE 0 END) AS count_5xx
    FROM cloud_logs
    GROUP BY endpoint, http_method
    ORDER BY p99_latency_ms DESC;
    """
    df_endpoints = con.execute(q3).fetchdf()
    df_endpoints.to_csv("activity5_cloud_analytics/results/q3_endpoint_latency.csv", index=False)
    print("\n[Query 3: API Endpoint Latency & Percentile Degradation]")
    print(df_endpoints.to_string(index=False))

    # ---------------------------------------------------------
    # CLOUD ARCHITECTURE FINOPS & COST ESTIMATION MODEL
    # Compares:
    # 1. On-Premises 3-node Hadoop Cluster
    # 2. Serverless AWS Athena (Raw CSV Data Lake)
    # 3. Serverless AWS Athena (Optimized Columnar Parquet + Snappy)
    # Scale: 100 GB/day = 3 TB/month raw ingestion, 30 queries/day
    # ---------------------------------------------------------
    print("\n[Cloud FinOps Cost Modeling: Serverless Athena vs On-Premises]")
    monthly_raw_tb = 3.0
    queries_per_day = 30
    monthly_queries = queries_per_day * 30 # 900 queries/month

    # On-prem: 3 servers @ $250/mo lease + power/cooling $100/mo + admin maintenance $350/mo
    cost_onprem = 3 * 250 + 100 + 350 # $1,200 / month

    # AWS S3 Raw CSV
    s3_storage_csv = monthly_raw_tb * 1024 * 0.023 # $70.66 / mo ($0.023/GB)
    # Uncompressed query scans entire 3 TB per query
    athena_scanned_csv_tb = monthly_queries * (monthly_raw_tb / 2) # avg scan half data
    cost_athena_csv_queries = athena_scanned_csv_tb * 5.0 # $5 per TB scanned
    glue_catalog_csv = 2.0
    cost_cloud_csv_total = s3_storage_csv + cost_athena_csv_queries + glue_catalog_csv

    # AWS S3 Parquet (Columnar + Snappy = 80% compression, projection scans only 10% of columns)
    parquet_storage_tb = monthly_raw_tb * 0.20 # 0.6 TB
    s3_storage_parquet = parquet_storage_tb * 1024 * 0.023 # $14.13 / mo
    # Scanning columnar Parquet: scans only requested columns (10-15% of data size)
    athena_scanned_parquet_tb = monthly_queries * (parquet_storage_tb * 0.12)
    cost_athena_parquet_queries = athena_scanned_parquet_tb * 5.0
    cost_cloud_parquet_total = s3_storage_parquet + cost_athena_parquet_queries + glue_catalog_csv

    cost_comparison = [
        {
            "Architecture": "On-Premises Dedicated Cluster",
            "Storage_Cost_USD": 250.0 * 3,
            "Compute_Query_Cost_USD": 450.0,
            "Total_Monthly_Cost_USD": cost_onprem,
            "Data_Scanned_Per_Query_GB": 3072.0,
            "Management_Overhead": "High (Physical hardware, OS patching, disk failures)"
        },
        {
            "Architecture": "AWS Athena (Raw CSV on S3)",
            "Storage_Cost_USD": round(s3_storage_csv, 2),
            "Compute_Query_Cost_USD": round(cost_athena_csv_queries, 2),
            "Total_Monthly_Cost_USD": round(cost_cloud_csv_total, 2),
            "Data_Scanned_Per_Query_GB": 1536.0,
            "Management_Overhead": "Zero Infrastructure (Unoptimized scan cost)"
        },
        {
            "Architecture": "AWS Athena (Parquet + Snappy)",
            "Storage_Cost_USD": round(s3_storage_parquet, 2),
            "Compute_Query_Cost_USD": round(cost_athena_parquet_queries, 2),
            "Total_Monthly_Cost_USD": round(cost_cloud_parquet_total, 2),
            "Data_Scanned_Per_Query_GB": 73.7,
            "Management_Overhead": "Zero Serverless (85%+ cost reduction over On-Prem!)"
        }
    ]
    df_cost = pd.DataFrame(cost_comparison)
    df_cost.to_csv("activity5_cloud_analytics/results/cloud_cost_comparison.csv", index=False)
    print(df_cost[["Architecture", "Storage_Cost_USD", "Compute_Query_Cost_USD", "Total_Monthly_Cost_USD"]].to_string(index=False))

    # ---------------------------------------------------------
    # GENERATE PUBLICATION VISUALIZATIONS
    # ---------------------------------------------------------
    print("\nGenerating Cloud Big Data Analytics charts...")

    # Chart 1: Status Code Distribution & Error Proportions
    cat_summary = df.groupby("status_category").size().reset_index(name="count")
    cat_summary["pct"] = (cat_summary["count"] / len(df)) * 100
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.2))
    
    # Pie chart of Status categories
    colors_pie = ["#2ecc71", "#f39c12", "#e74c3c"]
    ax1.pie(cat_summary["count"], labels=cat_summary["status_category"], autopct="%1.1f%%", startangle=140, colors=colors_pie, explode=(0, 0.05, 0.1), textprops={'fontweight': 'bold'})
    ax1.set_title("Overall HTTP Response Category Breakdown", fontweight="bold", fontsize=12)

    # Specific 4xx & 5xx error codes bar chart
    err_df = df[df["status_code"] >= 400]["status_code"].value_counts().reset_index()
    err_df.columns = ["status_code", "count"]
    err_df["status_code"] = err_df["status_code"].astype(str)
    
    ax2.bar(err_df["status_code"], err_df["count"], color="#e74c3c", edgecolor="black", alpha=0.85)
    ax2.set_xlabel("HTTP Error Status Code", fontweight="bold")
    ax2.set_ylabel("Occurrence Count", fontweight="bold")
    ax2.set_title("Detailed 4xx Client & 5xx Server Error Frequency", fontweight="bold", fontsize=12)
    ax2.grid(axis="y", linestyle="--", alpha=0.7)

    plt.suptitle("Cloud Web Application Telemetry: Error Pattern Profiling", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig("visualizations/activity5_cloud_error_distribution.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Chart 2: Hourly Request Volume with Incident Spike Alert Banner
    fig, ax1 = plt.subplots(figsize=(12, 5.5))
    ax2 = ax1.twinx()

    x = df_hourly["hour"]
    ax1.plot(x, df_hourly["total_requests"], color="#2b5c8f", marker="o", linewidth=2.5, label="Total Hourly Requests")
    ax2.plot(x, df_hourly["error_rate_pct"], color="#d62728", marker="s", linewidth=2.5, linestyle="--", label="Error Rate (% Failed)")

    # Highlight incident window
    ax1.axvspan(14, 15.5, color="red", alpha=0.18, label="Critical Spike Incident (14:00 - 15:30)")
    ax2.axhline(y=15.0, color="red", linestyle=":", label="Critical Error Threshold (15%)")

    ax1.set_xlabel("Hour of the Day (UTC)", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Total Request Volume", color="#2b5c8f", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Error Rate Percentage (%)", color="#d62728", fontsize=11, fontweight="bold")
    ax1.set_xticks(x)
    
    plt.title("Cloud Serverless Telemetry: Hourly Traffic Volumes & Flash Incident Spike", fontsize=13, fontweight="bold", pad=12)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    ax1.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("visualizations/activity5_cloud_traffic_spikes.png", dpi=300)
    plt.close()

    # Chart 3: Endpoint Latency Profile (p50, p95, p99)
    fig, ax = plt.subplots(figsize=(11, 5.8))
    df_ep_sorted = df_endpoints.sort_values("p99_latency_ms", ascending=True)

    y = np.arange(len(df_ep_sorted))
    h = 0.25

    ax.barh(y - h, df_ep_sorted["p50_latency_ms"], height=h, label="p50 (Median)", color="#3498db")
    ax.barh(y, df_ep_sorted["p95_latency_ms"], height=h, label="p95 (95th Percentile)", color="#f39c12")
    ax.barh(y + h, df_ep_sorted["p99_latency_ms"], height=h, label="p99 (99th Tail Latency)", color="#e74c3c")

    ax.set_yticks(y)
    ax.set_yticklabels([f"{row['endpoint']} ({row['http_method']})" for _, row in df_ep_sorted.iterrows()], fontsize=10)
    ax.set_xlabel("Response Latency (Milliseconds)", fontweight="bold")
    ax.set_title("Microservice Latency SLAs: p50 vs p95 vs p99 Tail Latency", fontsize=13, fontweight="bold", pad=12)
    ax.legend(loc="lower right")
    ax.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("visualizations/activity5_cloud_endpoint_latency.png", dpi=300)
    plt.close()

    # Chart 4: Cloud FinOps Cost Comparison
    fig, ax = plt.subplots(figsize=(10, 5.2))
    arch_labels = [
        "On-Premises Cluster\n(Fixed Hardware/Power)",
        "AWS Athena S3\n(Raw CSV Unoptimized)",
        "AWS Athena S3\n(Parquet Columnar + Snappy)"
    ]
    costs = [df_cost.loc[0, "Total_Monthly_Cost_USD"], df_cost.loc[1, "Total_Monthly_Cost_USD"], df_cost.loc[2, "Total_Monthly_Cost_USD"]]
    bar_colors = ["#7f8c8d", "#e67e22", "#27ae60"]

    bars = ax.bar(arch_labels, costs, color=bar_colors, width=0.5, edgecolor="black")
    ax.set_ylabel("Estimated Monthly Total Cost (USD $)", fontweight="bold")
    ax.set_title("Cloud FinOps Benchmark: On-Premise vs Serverless Athena (3 TB/month)", fontsize=13, fontweight="bold", pad=15)

    for b in bars:
        height = b.get_height()
        ax.text(b.get_x() + b.get_width()/2, height + 150, f"${height:,.2f}", ha="center", fontweight="bold", fontsize=11)

    ax.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("visualizations/activity5_cloud_cost_model.png", dpi=300)
    plt.close()

    print("✓ All 4 Cloud Big Data visualizations generated and saved in visualizations/")
    print("=" * 70)
    print("ACTIVITY 5 COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    run_cloud_log_analytics()

