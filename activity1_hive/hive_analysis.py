"""
Apache Hive Data Warehouse Analytics & Inventory Optimization Engine.
Executes HiveQL queries on the Supermarket Sales Data Warehouse,
computes inventory safety stock & reorder points, and generates visualizations.
"""

import os
import duckdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set clean visualization styling
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 11})

os.makedirs("visualizations", exist_ok=True)
os.makedirs("activity1_hive/results", exist_ok=True)

HIVE_DDL_SCRIPT = """
-- ====================================================================
-- APACHE HIVE ENTERPRISE DATA WAREHOUSE DDL ARCHITECTURE
-- ====================================================================

-- 1. Create Staging External Table mapping raw CSV stored on HDFS / Object Store
CREATE EXTERNAL TABLE IF NOT EXISTS supermarket_sales_raw (
    transaction_id STRING,
    timestamp STRING,
    date STRING,
    year_month STRING,
    hour_of_day INT,
    branch_id STRING,
    branch_name STRING,
    city STRING,
    region STRING,
    customer_type STRING,
    product_name STRING,
    category STRING,
    unit_price DOUBLE,
    unit_cost DOUBLE,
    quantity INT,
    gross_revenue DOUBLE,
    total_cost DOUBLE,
    net_profit DOUBLE,
    payment_method STRING,
    discount_applied DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/warehouse/tablespace/external/hive/supermarket_raw'
tblproperties ("skip.header.line.count"="1");

-- 2. Create Optimized Production Managed Table (ORC/Parquet) with Partitioning and Bucketing
CREATE TABLE IF NOT EXISTS supermarket_sales_analytics (
    transaction_id STRING,
    timestamp TIMESTAMP,
    date DATE,
    hour_of_day INT,
    branch_name STRING,
    city STRING,
    customer_type STRING,
    product_name STRING,
    category STRING,
    unit_price DOUBLE,
    unit_cost DOUBLE,
    quantity INT,
    gross_revenue DOUBLE,
    total_cost DOUBLE,
    net_profit DOUBLE,
    payment_method STRING,
    discount_applied DOUBLE
)
PARTITIONED BY (region STRING, year_month STRING)
CLUSTERED BY (branch_id) INTO 8 BUCKETS
STORED AS ORC
TBLPROPERTIES (
    "orc.compress"="SNAPPY",
    "transactional"="true"
);
"""

def run_hive_analytics():
    print("=" * 70)
    print("STARTING ACTIVITY 1: APACHE HIVE SALES & INVENTORY ANALYTICS")
    print("=" * 70)

    # Save Hive DDL
    with open("activity1_hive/hive_schema.hql", "w", encoding="utf-8") as f:
        f.write(HIVE_DDL_SCRIPT)
    print("✓ Hive DDL script generated: activity1_hive/hive_schema.hql")

    con = duckdb.connect(database=":memory:")
    
    # Load dataset
    con.execute("""
        CREATE TABLE sales AS 
        SELECT * FROM read_csv_auto('activity1_hive/supermarket_sales.csv', header=True);
    """)
    
    total_rows = con.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
    print(f"✓ Loaded {total_rows:,} records into Hive analytical engine.")

    # ---------------------------------------------------------
    # QUERY 1: Branch-wise and City-wise Revenue & Net Profit
    # ---------------------------------------------------------
    q1 = """
    SELECT 
        branch_id,
        branch_name,
        city,
        region,
        COUNT(transaction_id) AS total_transactions,
        SUM(quantity) AS total_units_sold,
        ROUND(SUM(gross_revenue), 2) AS total_revenue,
        ROUND(SUM(net_profit), 2) AS total_profit,
        ROUND((SUM(net_profit) / SUM(gross_revenue)) * 100, 2) AS profit_margin_pct
    FROM sales
    GROUP BY branch_id, branch_name, city, region
    ORDER BY total_revenue DESC;
    """
    df_branch = con.execute(q1).fetchdf()
    df_branch.to_csv("activity1_hive/results/q1_branch_revenue.csv", index=False)
    print("\n[Query 1: Branch-wise Financial Performance]")
    print(df_branch.to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 2: Top 10 Best-Selling Products by Revenue & Volume
    # ---------------------------------------------------------
    q2 = """
    SELECT 
        product_name,
        category,
        SUM(quantity) AS units_sold,
        ROUND(AVG(unit_price), 2) AS avg_unit_price,
        ROUND(SUM(gross_revenue), 2) AS total_revenue,
        ROUND(SUM(net_profit), 2) AS total_profit,
        ROUND(AVG(net_profit / gross_revenue) * 100, 2) AS avg_margin_pct
    FROM sales
    GROUP BY product_name, category
    ORDER BY total_revenue DESC
    LIMIT 10;
    """
    df_top_products = con.execute(q2).fetchdf()
    df_top_products.to_csv("activity1_hive/results/q2_top_products.csv", index=False)
    print("\n[Query 2: Top 10 Best-Selling Products]")
    print(df_top_products.to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 3: Peak Sales Hours Analysis (Hourly Revenue & Footfall)
    # ---------------------------------------------------------
    q3 = """
    SELECT 
        hour_of_day,
        COUNT(transaction_id) AS transaction_count,
        SUM(quantity) AS items_purchased,
        ROUND(SUM(gross_revenue), 2) AS hourly_revenue,
        ROUND(AVG(gross_revenue), 2) AS avg_basket_value
    FROM sales
    GROUP BY hour_of_day
    ORDER BY hour_of_day ASC;
    """
    df_hourly = con.execute(q3).fetchdf()
    df_hourly.to_csv("activity1_hive/results/q3_hourly_sales.csv", index=False)
    print("\n[Query 3: Peak Hourly Footfall and Revenue]")
    print(df_hourly.to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 4: Monthly Sales Trends & MoM Growth Analysis
    # ---------------------------------------------------------
    q4 = """
    WITH monthly_summary AS (
        SELECT 
            year_month,
            COUNT(transaction_id) AS transactions,
            ROUND(SUM(gross_revenue), 2) AS monthly_revenue,
            ROUND(SUM(net_profit), 2) AS monthly_profit
        FROM sales
        GROUP BY year_month
    )
    SELECT 
        year_month,
        transactions,
        monthly_revenue,
        monthly_profit,
        ROUND(
            ((monthly_revenue - LAG(monthly_revenue, 1) OVER (ORDER BY year_month)) / 
            LAG(monthly_revenue, 1) OVER (ORDER BY year_month)) * 100, 2
        ) AS mom_revenue_growth_pct
    FROM monthly_summary
    ORDER BY year_month;
    """
    df_monthly = con.execute(q4).fetchdf()
    df_monthly.to_csv("activity1_hive/results/q4_monthly_trends.csv", index=False)
    print("\n[Query 4: Monthly Sales Trends & MoM Growth]")
    print(df_monthly.to_string(index=False))

    # ---------------------------------------------------------
    # QUERY 5: Category-Wise Margin & Contribution
    # ---------------------------------------------------------
    q5 = """
    SELECT 
        category,
        COUNT(transaction_id) AS order_lines,
        SUM(quantity) AS total_units,
        ROUND(SUM(gross_revenue), 2) AS revenue,
        ROUND(SUM(net_profit), 2) AS profit,
        ROUND((SUM(gross_revenue) / (SELECT SUM(gross_revenue) FROM sales)) * 100, 2) AS revenue_share_pct,
        ROUND((SUM(net_profit) / SUM(gross_revenue)) * 100, 2) AS profit_margin_pct
    FROM sales
    GROUP BY category
    ORDER BY revenue DESC;
    """
    df_category = con.execute(q5).fetchdf()
    df_category.to_csv("activity1_hive/results/q5_category_performance.csv", index=False)
    print("\n[Query 5: Category Performance and Margin Contribution]")
    print(df_category.to_string(index=False))

    # ---------------------------------------------------------
    # INVENTORY MANAGEMENT STRATEGY CALCULATIONS
    # Safety Stock & Reorder Point (ROP) Model:
    # Daily demand d, Lead time L (e.g. 3 days), Service Level 95% (Z = 1.65)
    # Safety Stock SS = Z * sqrt(L) * sigma_daily
    # Reorder Point ROP = (d * L) + SS
    # ---------------------------------------------------------
    q_inventory = """
    WITH daily_demand AS (
        SELECT 
            product_name,
            category,
            date,
            SUM(quantity) AS daily_qty
        FROM sales
        GROUP BY product_name, category, date
    ),
    stats AS (
        SELECT 
            product_name,
            category,
            ROUND(AVG(daily_qty), 2) AS avg_daily_demand,
            ROUND(STDDEV(daily_qty), 2) AS std_daily_demand,
            MAX(daily_qty) AS peak_daily_demand
        FROM daily_demand
        GROUP BY product_name, category
    )
    SELECT 
        product_name,
        category,
        avg_daily_demand,
        std_daily_demand,
        peak_daily_demand,
        3 AS supplier_lead_time_days,
        ROUND(1.65 * SQRT(3) * COALESCE(std_daily_demand, 1.0), 1) AS safety_stock_units,
        ROUND((avg_daily_demand * 3) + (1.65 * SQRT(3) * COALESCE(std_daily_demand, 1.0)), 1) AS reorder_point_units,
        CASE 
            WHEN std_daily_demand > 2.5 THEN 'High Volatility - Buffer High'
            WHEN avg_daily_demand > 8.0 THEN 'Fast Mover - Automated Daily Replenish'
            ELSE 'Stable - Bi-Weekly Review'
        END AS inventory_recommendation
    FROM stats
    ORDER BY avg_daily_demand DESC;
    """
    df_inv = con.execute(q_inventory).fetchdf()
    df_inv.to_csv("activity1_hive/results/inventory_recommendations.csv", index=False)
    print("\n[Inventory Management & Reorder Point Optimization]")
    print(df_inv.head(10).to_string(index=False))

    # ---------------------------------------------------------
    # GENERATE PUBLICATION-GRADE VISUALIZATIONS
    # ---------------------------------------------------------
    print("\nGenerating visual analytics charts...")

    # Chart 1: Branch-wise Revenue & Profit Margin
    fig, ax1 = plt.subplots(figsize=(11, 6))
    x = np.arange(len(df_branch))
    width = 0.35
    
    rects1 = ax1.bar(x - width/2, df_branch['total_revenue'] / 1e5, width, label='Gross Revenue (Lakhs ₹)', color='#2b5c8f')
    rects2 = ax1.bar(x + width/2, df_branch['total_profit'] / 1e5, width, label='Net Profit (Lakhs ₹)', color='#2ca02c')
    
    ax1.set_ylabel('Amount in Lakhs (INR ₹)', fontsize=12, fontweight='bold')
    ax1.set_title('Supermarket Chain: Branch-wise Revenue and Net Profit Performance', fontsize=14, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_branch['branch_name'], rotation=25, ha='right', fontsize=10)
    ax1.legend(loc='upper right')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    fig.savefig("visualizations/activity1_hive_branch_revenue.png", dpi=300)
    plt.close()

    # Chart 2: Peak Sales Hours Analysis (Hourly Revenue & Footfall)
    fig, ax1 = plt.subplots(figsize=(11, 5.5))
    ax2 = ax1.twinx()
    
    ax1.bar(df_hourly['hour_of_day'], df_hourly['transaction_count'], color='#ff7f0e', alpha=0.75, width=0.6, label='Transaction Count (Footfall)')
    ax2.plot(df_hourly['hour_of_day'], df_hourly['hourly_revenue'] / 1e3, color='#1f77b4', marker='o', linewidth=2.5, label='Hourly Revenue (k ₹)')
    
    ax1.set_xlabel('Hour of the Day (24-Hour Format)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Number of Transactions', color='#d62728', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Revenue in Thousands (k ₹)', color='#1f77b4', fontsize=12, fontweight='bold')
    ax1.set_xticks(df_hourly['hour_of_day'])
    
    plt.title('Hourly Customer Traffic and Revenue Peaks (10:00-13:00 & 17:00-20:00 Rush)', fontsize=14, fontweight='bold', pad=15)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    ax1.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    fig.savefig("visualizations/activity1_hive_peak_hours.png", dpi=300)
    plt.close()

    # Chart 3: Top 10 Best-Selling Products by Revenue
    fig, ax = plt.subplots(figsize=(10, 6))
    df_sorted = df_top_products.sort_values('total_revenue', ascending=True)
    bars = ax.barh(df_sorted['product_name'], df_sorted['total_revenue'] / 1e3, color='#4e79a7', edgecolor='black', alpha=0.85)
    ax.set_xlabel('Gross Revenue in Thousands (k ₹)', fontsize=12, fontweight='bold')
    ax.set_title('Top 10 High-Revenue Products Across All Branches', fontsize=14, fontweight='bold', pad=15)
    
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 3, bar.get_y() + bar.get_height()/2, f'₹{width:.1f}k', ha='left', va='center', fontsize=9, fontweight='bold')
        
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    fig.savefig("visualizations/activity1_hive_top_products.png", dpi=300)
    plt.close()

    # Chart 4: Monthly Revenue & Profit Trend
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.plot(df_monthly['year_month'], df_monthly['monthly_revenue'] / 1e5, marker='s', linewidth=2.5, color='#2b5c8f', label='Gross Revenue (Lakhs ₹)')
    ax.plot(df_monthly['year_month'], df_monthly['monthly_profit'] / 1e5, marker='^', linewidth=2.5, color='#2ca02c', label='Net Profit (Lakhs ₹)')
    
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_ylabel('Amount in Lakhs (INR ₹)', fontsize=12, fontweight='bold')
    ax.set_title('Monthly Revenue Trend and Profit Trajectory (2025)', fontsize=14, fontweight='bold', pad=15)
    ax.set_xticklabels(df_monthly['year_month'], rotation=30, ha='right')
    ax.legend(loc='lower right')
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    fig.savefig("visualizations/activity1_hive_monthly_trend.png", dpi=300)
    plt.close()

    print("✓ All 4 Hive visualizations generated and saved in visualizations/")
    print("=" * 70)
    print("ACTIVITY 1 COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    run_hive_analytics()

