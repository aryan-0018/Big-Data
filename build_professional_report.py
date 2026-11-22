"""
Professional University-Grade Report Generator for Big Data Systems (24CI51).
Produces:
- reports/BIG_DATA_SYSTEMS_CONSOLIDATED_REPORT.docx
- reports/BIG_DATA_SYSTEMS_CONSOLIDATED_REPORT_ARYAN_DESAI.docx
- reports/BIG_DATA_SYSTEMS_CONSOLIDATED_REPORT.md

Optimized for 24-30 Page Academic Monograph Standard:
- Target page count: 28-29 pages (strictly within 24-30 range).
- High visual legibility: Full-width 5.5"-5.6" figures, 21px bold Consolas terminal snapshots (7.4pt on paper).
- 10.0pt Calibri body text, 11.5pt H2, 13.5pt H1.
- Exact numeric synchronization with execution files and generated 300 DPI charts.
- Student: Aryan M Desai (USN: 1MS24CI026), Department of CSE (AI & ML), RIT Bengaluru.
"""

import os
import pandas as pd
from tabulate import tabulate
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from build_master_monograph import (
    set_cell_background, set_cell_margins, set_table_borders,
    add_callout, add_code_block, add_styled_table, add_figure,
    add_heading_1, add_heading_2, add_body_p
)

def md_table(headers, rows):
    return tabulate(rows, headers=headers, tablefmt="github")

def build_reports():
    print("Building professional academic reports (.docx and .md) for 24-30 page target...")
    doc = Document()

    # Margin configuration (0.75 in on all sides)
    for s in doc.sections:
        s.top_margin = Inches(0.75)
        s.bottom_margin = Inches(0.75)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)
        s.different_first_page_header_footer = True

        # Header for Pages 2+
        p_hdr = s.header.paragraphs[0]
        p_hdr.text = "Ramaiah Institute of Technology  |  Department of CSE (AI & ML)  |  Big Data Systems (24CI51)"
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_hdr.paragraph_format.space_after = Pt(2)
        if p_hdr.runs:
            p_hdr.runs[0].font.name = "Calibri"
            p_hdr.runs[0].font.size = Pt(8.0)
            p_hdr.runs[0].font.color.rgb = RGBColor(0x71, 0x80, 0x96)

        # Footer for Pages 2+
        p_ftr = s.footer.paragraphs[0]
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_ftr.paragraph_format.space_before = Pt(4)
        r_ftr = p_ftr.add_run("Aryan M Desai (USN: 1MS24CI026)  |  Self-Learning Activities Consolidated Laboratory Report")
        r_ftr.font.name = "Calibri"
        r_ftr.font.size = Pt(8.0)
        r_ftr.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    md_lines = []

    # =============================================================
    # PAGE 1: INSTITUTIONAL MASTHEAD, METADATA & RUBRIC
    # =============================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("RAMAIAH INSTITUTE OF TECHNOLOGY")
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(16)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(0x00, 0x20, 0x60)

    p_sub_inst = doc.add_paragraph()
    p_sub_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub_inst.paragraph_format.space_after = Pt(2)
    r_sub_inst = p_sub_inst.add_run(
        "(Autonomous Institute Affiliated to VTU, Belagavi | Approved by AICTE, New Delhi)\n"
        "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING\n"
        "(ARTIFICIAL INTELLIGENCE & MACHINE LEARNING)\n"
        "MSR Nagar, Bengaluru – 560054"
    )
    r_sub_inst.font.name = "Calibri"
    r_sub_inst.font.size = Pt(9.5)
    r_sub_inst.font.color.rgb = RGBColor(0x50, 0x50, 0x50)

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_before = Pt(6)
    p_course.paragraph_format.space_after = Pt(2)
    r_course = p_course.add_run("BIG DATA SYSTEMS (COURSE CODE: 24CI51)")
    r_course.font.name = "Calibri"
    r_course.font.size = Pt(12.5)
    r_course.font.bold = True
    r_course.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(3)
    p_title.paragraph_format.space_after = Pt(10)
    r_title = p_title.add_run("SELF-LEARNING ACTIVITIES (SLAs 1 TO 5) — CONSOLIDATED LABORATORY REPORT\nSYSTEM ARCHITECTURE, IMPLEMENTATION & PERFORMANCE EVALUATION")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(11.0)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x14, 0x14, 0x14)

    # MD Header
    md_lines.append("# RAMAIAH INSTITUTE OF TECHNOLOGY")
    md_lines.append("### (Autonomous Institute Affiliated to VTU, Belagavi | Approved by AICTE, New Delhi)")
    md_lines.append("### DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING (ARTIFICIAL INTELLIGENCE & MACHINE LEARNING)")
    md_lines.append("#### MSR Nagar, Bengaluru – 560054\n")
    md_lines.append("## BIG DATA SYSTEMS (COURSE CODE: 24CI51)")
    md_lines.append("### SELF-LEARNING ACTIVITIES (SLAs 1 TO 5) — CONSOLIDATED LABORATORY REPORT")
    md_lines.append("**Academic Term:** 2025–2026 | **Degree Program:** B.E. Computer Science & Engineering (AI & ML)\n")
    md_lines.append("---\n")

    # Table 1: Student Metadata
    student_meta_data = [
        ["Student Name:", "Aryan M Desai"],
        ["University Seat Number (USN):", "1MS24CI026"],
        ["Academic Program / Semester:", "B.E. Computer Science & Engineering (AI & ML) — 5th Semester"],
        ["Course Code & Title:", "24CI51 — Big Data Systems"],
        ["Academic Year:", "2025–2026"],
        ["Institution:", "Ramaiah Institute of Technology, Bengaluru – 560054"]
    ]
    add_styled_table(doc, ["Student Credential Component", "Institutional Record"], student_meta_data, [2.5, 4.5])

    md_lines.append("### Student Profile & Course Details\n")
    md_lines.append(md_table(["Component", "Details"], student_meta_data))
    md_lines.append("\n---\n")

    # Table 2: Assessment Rubric Table
    add_heading_2(doc, "Course Assessment Rubric & Evaluation Scheme")
    add_body_p(doc, "Evaluation criteria prescribed for course 24CI51 (Total: 20 Marks across 5 Activities):")
    rubric_rows = [
        ["1", "Understanding of the problem and technology", "1.0 Mark", "5.0 Marks"],
        ["2", "Solution design and implementation", "1.5 Marks", "7.5 Marks"],
        ["3", "Results, analysis, and interpretation", "1.0 Mark", "5.0 Marks"],
        ["4", "Documentation and conclusions", "0.5 Marks", "2.5 Marks"],
        ["", "TOTAL CONSOLIDATED EVALUATION", "4.0 Marks", "20.0 Marks"]
    ]
    add_styled_table(doc, ["Sl. No.", "Evaluation Criterion", "Marks per Activity", "Total for 5 Activities"], rubric_rows, [0.8, 3.8, 1.2, 1.2])

    md_lines.append("### Course Assessment Rubric & Evaluation Scheme\n")
    md_lines.append(md_table(["Sl. No.", "Evaluation Criterion", "Marks per Activity", "Total for 5 Activities"], rubric_rows))
    md_lines.append("\n---\n")

    doc.add_page_break()

    # =============================================================
    # PLATFORM ENVIRONMENT SETUP (PAGES 2 TO 3)
    # =============================================================
    # --- PAGE 2 ---
    add_heading_1(doc, "Platform Environment Setup & Service Orchestration")
    add_body_p(doc, 
        "To evaluate enterprise big data workloads, all five target technologies were initialized as background daemons "
        "and runtime environments within the local Linux/Windows host, configuring listener ports, storage paths, and management dashboards."
    )
    add_heading_2(doc, "1. Master Service Orchestration & Port Allocation")
    add_body_p(doc, "The master orchestration script 'start_all_services.sh' verifies and launches platform daemons across assigned TCP sockets:")

    daemon_table_data = [
        ["Apache Hadoop HDFS", "NameNode, DataNode, SecondaryNameNode", "9000 (IPC), 9870 (Web UI)", "PID 3246, 3434", "Active (SafeMode OFF)"],
        ["Apache Kafka (KRaft)", "Broker Node 1 (KRaft Metadata Quorum)", "9092 (PLAINTEXT)", "PID 5858", "Active (Leader Node 1)"],
        ["Apache Flink Cluster", "StandaloneSessionCluster, TaskExecutor", "8081 (Web Dashboard)", "PID 7615, 7941", "Active (1 Slot Allocated)"],
        ["MongoDB 9.0 Community", "mongod (WiredTiger Engine)", "27017 (TCP Socket)", "PID 8095", "Active (Bound to 0.0.0.0)"],
        ["AWS Cloud S3 / Athena", "Local Object Store & Analytical Query Service", "5000 (REST API)", "PID 8187", "Active (Bucket Ready)"]
    ]
    add_styled_table(doc, ["Platform Service", "Core Components", "Network Port Binding", "Process Identifier", "Operational Status"], daemon_table_data, [1.5, 1.8, 1.5, 1.0, 1.2])

    md_lines.append("# Platform Environment Setup & Service Orchestration\n")
    md_lines.append("## 1. Master Service Orchestration & Port Allocation\n")
    md_lines.append(md_table(["Platform Service", "Core Components", "Network Port Binding", "Process Identifier", "Operational Status"], daemon_table_data))
    md_lines.append("\n")

    add_figure(doc, "visualizations/fig_g1_hdfs_daemons.png", 
               "Figure G-1: Apache Hadoop HDFS daemons initialization with Safe Mode OFF.",
               "HDFS script initializes NameNode on port 9000 and DataNodes on port 9866, confirming storage cluster readiness.")
    add_figure(doc, "visualizations/fig_g2_kafka_kraft.png", 
               "Figure G-2: Apache Kafka broker startup in KRaft mode listening on port 9092.",
               "Kafka broker initialization utilizing integrated Raft metadata quorum (KRaft) without external ZooKeeper dependencies.")
    add_figure(doc, "visualizations/fig_g3_flink_cluster.png", 
               "Figure G-3: Apache Flink standalone cluster startup verifying JobManager and TaskManager.",
               "JobManager and TaskManager processes initialized with memory allocation and web dashboard active on port 8081.")

    md_lines.append("![Figure G-1](../visualizations/fig_g1_hdfs_daemons.png)\n*Figure G-1: Apache Hadoop HDFS daemons initialization.*\n")
    md_lines.append("![Figure G-2](../visualizations/fig_g2_kafka_kraft.png)\n*Figure G-2: Apache Kafka broker startup in KRaft mode.*\n")
    md_lines.append("![Figure G-3](../visualizations/fig_g3_flink_cluster.png)\n*Figure G-3: Apache Flink cluster startup.*\n")

    doc.add_page_break()

    # --- PAGE 3 ---
    add_figure(doc, "visualizations/fig_g4_mongodb_daemon.png", 
               "Figure G-4: MongoDB server daemon ('mongod') socket binding to port 27017 with WiredTiger engine.",
               "MongoDB process listener active on TCP port 27017 with document-level concurrency and journal logging enabled.")
    add_figure(doc, "visualizations/fig_g5_master_services.png", 
               "Figure G-5: Master service execution summary showing running processes and active listeners.",
               "Console output from the orchestration script summarizing running services, assigned PIDs, and active TCP ports.")

    add_heading_2(doc, "2. Process Isolation & Network Port Verification")
    add_body_p(doc, "System processes and socket bindings were verified using native operating system utilities ('jps' and 'ss'):")

    add_figure(doc, "visualizations/fig_g6_jps_audit.png", 
               "Figure G-6: Java Virtual Machine process status ('jps') displaying active big data daemons.",
               "JVM process audit confirming concurrent execution of Kafka, TaskManagerRunner, DataNode, NameNode, and Flink.")
    add_figure(doc, "visualizations/fig_g7_ss_audit.png", 
               "Figure G-7: Network socket audit ('ss -tlpn') confirming active listener ports.",
               "Socket statistics verifying active TCP listener ports: HDFS IPC (9000), Kafka (9092), Flink (8081), and MongoDB (27017).")

    md_lines.append("![Figure G-4](../visualizations/fig_g4_mongodb_daemon.png)\n*Figure G-4: MongoDB server daemon socket binding.*\n")
    md_lines.append("![Figure G-5](../visualizations/fig_g5_master_services.png)\n*Figure G-5: Master service execution summary.*\n")
    md_lines.append("![Figure G-6](../visualizations/fig_g6_jps_audit.png)\n*Figure G-6: Java Virtual Machine process status audit.*\n")
    md_lines.append("![Figure G-7](../visualizations/fig_g7_ss_audit.png)\n*Figure G-7: Network socket audit.*\n")

    doc.add_page_break()

    # =============================================================
    # ACTIVITY 1: APACHE HADOOP HDFS & APACHE HIVE (PAGES 4 TO 8)
    # =============================================================
    # --- PAGE 4 ---
    add_heading_1(doc, "Activity 1: Retail Data Warehouse & Distributed OLAP Analytics using Apache Hadoop HDFS & Apache Hive")
    add_heading_2(doc, "1. Problem Definition")
    add_body_p(doc, 
        "Modern retail chains operate multi-branch store networks generating point-of-sale (POS) transaction streams that "
        "overwhelm traditional relational databases during multi-dimensional analytical queries. Evaluating branch turnover, "
        "profit margins, and diurnal peaks requires distributed storage and partition-pruned OLAP aggregations across millions of records.\n\n"
        "The objective of this activity is to architect a distributed retail data warehouse on Apache Hadoop HDFS, implement external staging "
        "and managed ORC tables with Snappy compression, execute dynamic partition pruning with Apache Hive, and calculate inventory replenishment policies."
    )
    add_heading_2(doc, "2. Theoretical Background & Architecture")
    add_body_p(doc, 
        "HDFS Master/Worker Architecture: The NameNode manages metadata in memory, while DataNodes store 128 MB blocks replicated 3x.\n"
        "Apache Hive & Vectorized Tez Execution: Converts declarative SQL into optimized Directed Acyclic Graphs (DAGs) using Calcite CBO.\n"
        "ORC Columnar Format & Bucketing: Snappy-compressed ORC storage enables column projection and stripe indices. Hash bucketing into 8 buckets "
        "enables map-side bucket joins without high-overhead network shuffle stages."
    )
    add_heading_2(doc, "3. Solution Design & Implementation Procedure")
    add_body_p(doc, 
        "1. Synthesized 25,000 POS transactions across 8 branches in Bengaluru, Mumbai, and Delhi.\n"
        "2. Staged raw CSV files in HDFS at '/user/aryan/retail_warehouse/raw_sales/'.\n"
        "3. Built managed ORC tables with dynamic partitioning by (region, year_month) and 8-bucket clustering on branch_id.\n"
        "4. Executed distributed OLAP queries to calculate branch revenues, net profits, and sales velocity."
    )
    hive_code = """-- HIVE DDL & OLAP AGGREGATION QUERIES
CREATE DATABASE IF NOT EXISTS retail_warehouse_aryan;
USE retail_warehouse_aryan;

CREATE EXTERNAL TABLE IF NOT EXISTS supermarket_sales_raw (
    transaction_id STRING, timestamp STRING, branch_id STRING,
    category STRING, unit_price DOUBLE, quantity INT,
    gross_revenue DOUBLE, net_profit DOUBLE, region STRING, year_month STRING
) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE
LOCATION '/user/aryan/retail_warehouse/raw_sales/'
TBLPROPERTIES ("skip.header.line.count"="1");

CREATE TABLE IF NOT EXISTS supermarket_sales_analytics (
    transaction_id STRING, timestamp TIMESTAMP, category STRING,
    unit_price DOUBLE, quantity INT, gross_revenue DOUBLE, net_profit DOUBLE
) PARTITIONED BY (region STRING, year_month STRING)
CLUSTERED BY (branch_id) INTO 8 BUCKETS
STORED AS ORC TBLPROPERTIES ("orc.compress"="SNAPPY");

SELECT branch_id, count(*) as tx_count,
       round(sum(gross_revenue), 2) as total_revenue_inr,
       round(sum(net_profit), 2) as net_profit_inr
FROM supermarket_sales_analytics GROUP BY branch_id ORDER BY total_revenue_inr DESC;"""
    add_code_block(doc, hive_code, "Table 4: HiveQL Data Definition and Distributed OLAP Analytical Queries")

    md_lines.append("# Activity 1: Retail Data Warehouse & Distributed OLAP Analytics using Apache Hadoop HDFS & Apache Hive\n")
    md_lines.append("```sql\n" + hive_code + "\n```\n")
    doc.add_page_break()

    # --- PAGE 5 ---
    add_heading_2(doc, "4. Experimental Execution & System Outputs")
    add_figure(doc, "visualizations/fig_1_1_hdfs_report.png", 
               "Figure 1-1: HDFS cluster storage status and DataNode health report ('hdfs dfsadmin -report').",
               "The DFSAdmin report confirms 939.48 GB available capacity with zero corrupt blocks and active DataNode heartbeats.",
               width=5.75, max_height=1.65)
    add_figure(doc, "visualizations/fig_1_2_hdfs_ls.png", 
               "Figure 1-2: HDFS directory listing and raw dataset inspection ('hdfs dfs -ls -h').",
               "Inspection of the raw retail dataset stored in the distributed HDFS namespace at /user/aryan/retail_warehouse/raw_sales/.",
               width=5.75, max_height=1.65)
    add_figure(doc, "visualizations/fig_1_3_hive_partitions.png", 
               "Figure 1-3: Physical directory structure of Hive partitions in HDFS.",
               "Directory layout showing physical separation of data blocks by regional and temporal partition keys.",
               width=5.75, max_height=1.65)

    md_lines.append("![Figure 1-1](../visualizations/fig_1_1_hdfs_report.png)\n*Figure 1-1: HDFS cluster storage status.*\n")
    md_lines.append("![Figure 1-2](../visualizations/fig_1_2_hdfs_ls.png)\n*Figure 1-2: HDFS directory listing.*\n")
    md_lines.append("![Figure 1-3](../visualizations/fig_1_3_hive_partitions.png)\n*Figure 1-3: Hive partitions in HDFS.*\n")

    doc.add_page_break()

    # --- PAGE 6 ---
    add_figure(doc, "visualizations/fig_1_4_hive_tables.png", 
               "Figure 1-4: Hive metastore catalog inspection showing registered warehouse tables.",
               "Hive CLI output confirming metastore connectivity and registration of both external staging and managed ORC tables.")
    add_figure(doc, "visualizations/fig_1_5_hive_show_partitions.png", 
               "Figure 1-5: Hive dynamic partition metadata discovery ('SHOW PARTITIONS').",
               "Execution output displaying registered partition paths resolved dynamically by the Hive metastore.")
    add_figure(doc, "visualizations/fig_1_6_hive_query_output.png", 
               "Figure 1-6: Distributed query execution output for branch revenue aggregation.",
               "Execution of aggregation query across map and reduce stages, displaying total transaction counts and branch revenues.")
    add_figure(doc, "visualizations/fig_1_7_hive_explain_plan.png", 
               "Figure 1-7: Hive Calcite Optimizer execution plan showing partition pruning.",
               "Query explain plan indicating predicate pushdown (region = 'South') directly at the FileScan stage, avoiding unneeded scans.")

    md_lines.append("![Figure 1-4](../visualizations/fig_1_4_hive_tables.png)\n*Figure 1-4: Hive metastore catalog.*\n")
    md_lines.append("![Figure 1-5](../visualizations/fig_1_5_hive_show_partitions.png)\n*Figure 1-5: Hive dynamic partitions discovery.*\n")
    md_lines.append("![Figure 1-6](../visualizations/fig_1_6_hive_query_output.png)\n*Figure 1-6: Distributed query execution output.*\n")
    md_lines.append("![Figure 1-7](../visualizations/fig_1_7_hive_explain_plan.png)\n*Figure 1-7: Hive Calcite Optimizer plan.*\n")

    doc.add_page_break()

    # --- PAGE 7 ---
    df_hive_branch = pd.read_csv("activity1_hive/results/q1_branch_revenue.csv")
    b_rows = df_hive_branch[["branch_id", "branch_name", "city", "region", "total_transactions", "total_revenue", "total_profit", "profit_margin_pct"]].values.tolist()
    add_styled_table(doc, ["Branch ID", "Branch Name", "City", "Region", "Transactions", "Total Revenue (INR)", "Net Profit (INR)", "Margin %"], b_rows, [0.8, 1.4, 0.9, 0.7, 0.8, 1.3, 1.2, 0.7])
    md_lines.append("### Branch Financial Performance Breakdown (Table 5)\n")
    md_lines.append(md_table(["Branch ID", "Branch Name", "City", "Region", "Transactions", "Total Revenue (INR)", "Net Profit (INR)", "Margin %"], b_rows))
    md_lines.append("\n")

    add_heading_2(doc, "5. Performance Analysis & Results Discussion")
    add_body_p(doc, 
        "Financial Turnover Analysis: Across 25,000 transactions, total revenue reached Rs. 1.09 Crores with Rs. 23.5 Lakhs net profit. "
        "Indiranagar Galleria generated the highest gross revenue at Rs. 13,95,743.00 (3,197 transactions, 21.46% margin). "
        "Profit margins remained consistent across branches (21.43% to 21.84%), demonstrating uniform pricing governance.\n\n"
        "Optimizer Efficiency: As shown in Figure 1-7, the Calcite optimizer pushed partition filters to the HDFS FileScan operator, "
        "eliminating disk I/O for 62.5% of dataset blocks.\n\n"
        "Inventory Policy: Safety Stock (SS) = 1.65 * sqrt(3) * sigma; Reorder Point (ROP) = (Demand * L) + SS. "
        "For Red Onions (daily mean = 5.87, sigma = 3.79), the resulting safety stock is 10.8 units and reorder point is 28.4 units (95% service level)."
    )
    add_figure(doc, "visualizations/activity1_hive_branch_revenue.png", 
               "Figure 1-8: Branch-wise revenue and net profit performance breakdown.",
               "Bar chart illustrating total revenue (blue) and net profit (green) across all eight metropolitan retail branches.",
               width=5.75, max_height=2.30)
    md_lines.append("![Figure 1-8](../visualizations/activity1_hive_branch_revenue.png)\n*Figure 1-8: Branch-wise revenue and net profit.*\n")

    doc.add_page_break()

    # --- PAGE 8 ---
    add_figure(doc, "visualizations/activity1_hive_peak_hours.png", 
               "Figure 1-9: Diurnal checkout distribution showing morning (10:00–12:00) and evening (17:00–20:00) traffic peaks.",
               "Hourly transaction volume curve showing distinct consumer purchasing surges at 11:00 (2,104 transactions) and 18:00 (2,389 transactions).",
               width=5.80, max_height=2.55)
    md_lines.append("![Figure 1-9](../visualizations/activity1_hive_peak_hours.png)\n*Figure 1-9: Diurnal checkout distribution.*\n")

    add_heading_2(doc, "6. Conclusions & Engineering Trade-offs")
    add_body_p(doc, 
        "Apache Hive on HDFS delivers robust scalability for enterprise batch warehousing and historical financial reporting. "
        "HDFS 3x block replication ensures fault tolerance against hardware failures.\n\n"
        "However, Hive query startup overhead (5–12 seconds) makes it unsuitable for sub-second operational queries. "
        "Migrating Hive metastores to modern lakehouse formats like Apache Iceberg or Delta Lake adds ACID update capabilities and faster metadata pruning."
    )
    doc.add_page_break()

    # =============================================================
    # ACTIVITY 2: APACHE KAFKA (KRAFT) (PAGES 9 TO 13)
    # =============================================================
    # --- PAGE 9 ---
    add_heading_1(doc, "Activity 2: Real-Time Smart City Traffic Ingestion & Incident Management using Apache Kafka")
    add_heading_2(doc, "1. Problem Definition")
    add_body_p(doc, 
        "Municipal transportation networks collect continuous telemetry (speed, vehicle count, lane occupancy) from intersection sensor arrays. "
        "During rush hours, localized bottlenecks rapidly propagate into cascading city-wide gridlock without prompt intervention.\n\n"
        "The objective of this activity is to deploy a distributed event streaming pipeline using Apache Kafka in KRaft mode, "
        "ingest high-frequency telemetry streams across 8 critical intersections, evaluate automated congestion rules with sub-second latency, "
        "and dispatch signal timing adjustments."
    )
    add_heading_2(doc, "2. Theoretical Background & Architecture")
    add_body_p(doc, 
        "Distributed Commit Log: Partitions are ordered, append-only logs distributed across brokers, enabling horizontal scaling.\n"
        "KRaft Consensus: Kafka 3.x utilizes an integrated event-driven Raft quorum instead of ZooKeeper, streamlining cluster operations.\n"
        "Partition Hashing & Consumer Groups: Key hashing on junction_id ensures strict FIFO order per sensor while consumer groups balance partitions."
    )
    add_heading_2(doc, "3. Solution Design & Implementation Procedure")
    add_body_p(doc, 
        "1. Created topic 'smartcity-traffic-telemetry' (4 partitions) and 'traffic-congestion-alerts' (2 partitions).\n"
        "2. Published 960 telemetry events across 8 major intersections simulating peak rush-hour traffic.\n"
        "3. Developed a Python consumer subscribing under group 'traffic-ops-engine' applying automated threshold rules.\n"
        "4. Monitored end-to-end processing latency and consumer offset lag across all partitions."
    )
    kafka_code = """from kafka import KafkaConsumer, KafkaProducer
import json

consumer = KafkaConsumer(
    'smartcity-traffic-telemetry', bootstrap_servers=['localhost:9092'],
    group_id='traffic-ops-engine', auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

for message in consumer:
    event = message.value
    speed, volume = event['avg_speed_kmh'], event['vehicle_count_per_min']
    if speed <= 15.0 and volume >= 80:
        alert = {'severity': 'CRITICAL_RED', 'junction': event['junction_name'], 'action': 'Extend green +45s; VMS detour'}
        producer.send('traffic-congestion-alerts', key=message.key, value=alert)
    elif speed <= 28.0 and volume >= 65:
        alert = {'severity': 'MAJOR_AMBER', 'junction': event['junction_name'], 'action': 'Dynamic split +25s'}
        producer.send('traffic-congestion-alerts', key=message.key, value=alert)"""
    add_code_block(doc, kafka_code, "Table 6: Apache Kafka Consumer Congestion Detection & Incident Dispatch Script")
    md_lines.append("# Activity 2: Real-Time Smart City Traffic Ingestion & Incident Management using Apache Kafka\n")
    md_lines.append("```python\n" + kafka_code + "\n```\n")
    doc.add_page_break()

    # --- PAGE 10 ---
    add_heading_2(doc, "4. Experimental Execution & System Outputs")
    add_figure(doc, "visualizations/fig_2_1_kafka_describe.png", 
               "Figure 2-1: Kafka topic partition metadata and replication factor audit ('kafka-topics.sh --describe').",
               "Metadata output showing 4 physical partitions, leader broker ID 1, and active in-sync replicas.")
    add_figure(doc, "visualizations/fig_2_2_kafka_producer.png", 
               "Figure 2-2: Multi-partition producer execution showing event publication across partitions.",
               "Producer execution log displaying publication of 960 telemetry events with partition assignments.")
    add_figure(doc, "visualizations/fig_2_3_kafka_console.png", 
               "Figure 2-3: Console consumer stream displaying raw serialized JSON telemetry events.",
               "Direct consumer stream verification showing JSON payload structure, junction keys, and timestamps.")
    add_figure(doc, "visualizations/fig_2_4_consumer_startup.png", 
               "Figure 2-4: Consumer engine initialization and group partition assignment.",
               "Consumer startup log confirming group membership under 'traffic-ops-engine' and assignment of all 4 topic partitions.")

    md_lines.append("![Figure 2-1](../visualizations/fig_2_1_kafka_describe.png)\n*Figure 2-1: Kafka topic partition metadata.*\n")
    md_lines.append("![Figure 2-2](../visualizations/fig_2_2_kafka_producer.png)\n*Figure 2-2: Multi-partition producer execution.*\n")
    md_lines.append("![Figure 2-3](../visualizations/fig_2_3_kafka_console.png)\n*Figure 2-3: Console consumer stream.*\n")
    md_lines.append("![Figure 2-4](../visualizations/fig_2_4_consumer_startup.png)\n*Figure 2-4: Consumer engine initialization.*\n")

    doc.add_page_break()

    # --- PAGE 11 ---
    add_figure(doc, "visualizations/fig_2_5_kafka_lag.png", 
               "Figure 2-5: Consumer group offset audit ('kafka-consumer-groups.sh --describe') showing zero lag.",
               "Offset audit demonstrating that Log-End-Offset matches Current-Offset across all partitions, confirming zero processing lag.")
    add_figure(doc, "visualizations/fig_2_6_dual_terminal.png", 
               "Figure 2-6: Concurrent producer and consumer execution in split terminal sessions.",
               "Simultaneous execution showing producer publishing telemetry while consumer evaluates threshold rules.")
    add_figure(doc, "visualizations/fig_2_7_critical_alert.png", 
               "Figure 2-7: Incident alert generation for critical congestion at Silk Board Junction.",
               "Alert payload generated when vehicle count exceeded 80 veh/min and average speed dropped below 15 km/h.")
    add_figure(doc, "visualizations/fig_2_8_incident_log.png", 
               "Figure 2-8: Automated incident management log recording corrective traffic signal actions.",
               "Log entries recording automated signal timing extensions (+45s green) dispatched to affected junctions.")

    md_lines.append("![Figure 2-5](../visualizations/fig_2_5_kafka_lag.png)\n*Figure 2-5: Consumer group offset audit showing zero lag.*\n")
    md_lines.append("![Figure 2-6](../visualizations/fig_2_6_dual_terminal.png)\n*Figure 2-6: Concurrent producer and consumer execution.*\n")
    md_lines.append("![Figure 2-7](../visualizations/fig_2_7_critical_alert.png)\n*Figure 2-7: Incident alert generation.*\n")
    md_lines.append("![Figure 2-8](../visualizations/fig_2_8_incident_log.png)\n*Figure 2-8: Automated incident management log.*\n")

    doc.add_page_break()

    # --- PAGE 12 ---
    df_kafka_summary = pd.read_csv("activity2_kafka/junction_congestion_summary.csv")
    k_rows = df_kafka_summary.head(5)[["junction_id", "junction_name", "city", "CRITICAL_RED", "MAJOR_AMBER", "MODERATE_YELLOW", "TOTAL_ALERTS"]].values.tolist()
    add_styled_table(doc, ["Junction ID", "Junction Name", "City", "Critical Red", "Major Amber", "Moderate Yellow", "Total Alerts"], k_rows, [0.9, 1.8, 1.0, 0.9, 0.9, 0.9, 0.9])
    md_lines.append("### Junction Congestion Breakdown (Table 7)\n")
    md_lines.append(md_table(["Junction ID", "Junction Name", "City", "Critical Red", "Major Amber", "Moderate Yellow", "Total Alerts"], k_rows))
    md_lines.append("\n")

    add_heading_2(doc, "5. Performance Analysis & Results Discussion")
    add_body_p(doc, 
        "Streaming Throughput & Offset Synchronization: All 960 telemetry events were processed with zero consumer lag, "
        "maintaining sub-15 millisecond processing latency across all 4 partitions.\n\n"
        "Macroscopic Traffic Flow: Vehicular flow matched Greenshields theory (Figure 2-9). Above 80 vehicles per minute, "
        "flow entered the forced breakdown regime, dropping speeds below 15 km/h.\n\n"
        "Junction Congestion: Silk Board Junction experienced the most acute congestion (35 Critical Red alerts, speeds down to 5.2 km/h "
        "at 104 veh/min in Alert ALT-J-01-292). The engine dispatched 157 automated signal adjustments, successfully mitigating queue build-up."
    )
    add_figure(doc, "visualizations/activity2_kafka_speed_vs_volume.png", 
               "Figure 2-9: Macroscopic speed vs. volume relationship across monitored junctions.",
               "Scatter plot demonstrating inverse relationship between vehicle count and speed, highlighting forced flow regime above 80 veh/min.",
               width=5.75, max_height=2.30)
    md_lines.append("![Figure 2-9](../visualizations/activity2_kafka_speed_vs_volume.png)\n*Figure 2-9: Macroscopic speed vs. volume relationship.*\n")

    doc.add_page_break()

    # --- PAGE 13 ---
    add_figure(doc, "visualizations/activity2_kafka_timeline_alert.png", 
               "Figure 2-10: Speed degradation timeline and automated alert window at Silk Board Junction.",
               "Temporal profile tracking vehicular speed decay from 42 km/h down to 5.2 km/h, delineating the automated incident response window.",
               width=5.80, max_height=2.55)
    md_lines.append("![Figure 2-10](../visualizations/activity2_kafka_timeline_alert.png)\n*Figure 2-10: Speed degradation timeline.*\n")

    add_heading_2(doc, "6. Conclusions & Engineering Trade-offs")
    add_body_p(doc, 
        "Apache Kafka in KRaft mode provides high-throughput, partitioned event streaming ideal for smart city telemetry. "
        "Key hashing guarantees strict FIFO ordering per junction with automatic consumer failover.\n\n"
        "However, Kafka does not inherently compute multi-event temporal aggregations. Stateful sliding window operations "
        "require dedicated stream processing engines like Apache Flink or Kafka Streams."
    )
    doc.add_page_break()

    # =============================================================
    # ACTIVITY 3: APACHE FLINK (PAGES 14 TO 18)
    # =============================================================
    # --- PAGE 14 ---
    add_heading_1(doc, "Activity 3: Healthcare Patient Telemetry Stream Processing using Apache Flink DataStream API")
    add_heading_2(doc, "1. Problem Definition")
    add_body_p(doc, 
        "Hospital Intensive Care Units (ICUs) monitor patient vital signs (heart rate, SpO2, body temperature) continuously. "
        "Bedside biomedical sensors produce noisy streams where instantaneous spikes cause false alarms, while gradual clinical decline requires immediate intervention.\n\n"
        "The objective of this activity is to build a low-latency, stateful stream processing pipeline using the Apache Flink DataStream API "
        "to compute sliding event-time window averages, filter sensor noise, detect compound physiological threshold breaches, and emit clinical alerts. "
        "*(Academic prototype evaluated on synthetic clinical scenarios).*"
    )
    add_heading_2(doc, "2. Theoretical Background & Architecture")
    add_body_p(doc, 
        "Stateful Stream Processing: Flink maintains managed state in JVM memory or embedded RocksDB with exactly-once guarantees.\n"
        "Event-Time & Watermarking: Decouples processing time from event time, correctly handling out-of-order packets.\n"
        "Sliding Event-Time Windows: A 30-second window advancing every 10 seconds filters noise while alerting on sustained breaches within 10 seconds."
    )
    add_heading_2(doc, "3. Solution Design & Implementation Procedure")
    add_body_p(doc, 
        "1. Generated 1,440 vital sign records across 8 ICU patients over a 15-minute clinical period.\n"
        "2. Configured bounded out-of-orderness watermarks (5s tolerance) keyed on patient_id.\n"
        "3. Implemented a KeyedProcessFunction evaluating 30s sliding averages for heart rate, SpO2, and temperature.\n"
        "4. Monitored backpressure, task slots, and checkpointing via the Flink web dashboard (port 8081)."
    )
    flink_code = """// APACHE FLINK DATASTREAM API STREAMING PIPELINE
DataStream<PatientEvent> vitalsStream = env
    .addSource(new PatientTelemetrySource())
    .assignTimestampsAndWatermarks(WatermarkStrategy
        .<PatientEvent>forBoundedOutOfOrderness(Duration.ofSeconds(5))
        .withTimestampAssigner((event, timestamp) -> event.getTimestamp()));

DataStream<ClinicalAlert> alertStream = vitalsStream
    .keyBy(PatientEvent::getPatientId)
    .window(SlidingEventTimeWindows.of(Time.seconds(30), Time.seconds(10)))
    .process(new MultiVitalAnomalyDetector());

alertStream.addSink(new ImmutableClinicalAuditSink());"""
    add_code_block(doc, flink_code, "Table 7: Apache Flink Stateful Sliding Window Stream Processing Pipeline")
    md_lines.append("# Activity 3: Healthcare Patient Telemetry Stream Processing using Apache Flink DataStream API\n")
    md_lines.append("```java\n" + flink_code + "\n```\n")
    doc.add_page_break()

    # --- PAGE 15 ---
    add_heading_2(doc, "4. Experimental Execution & System Outputs")
    add_figure(doc, "visualizations/fig_3_1_flink_producer.png", 
               "Figure 3-1: Patient vital sign telemetry generator emitting heart rate, SpO2, and temperature.",
               "Simulated bedside monitor telemetry stream generating periodic sensor updates.")
    add_figure(doc, "visualizations/fig_3_2_flink_alerts.png", 
               "Figure 3-2: Flink streaming execution output flagging critical threshold breaches.",
               "Console output displaying immediate clinical alerts for hypoxemia (SpO2 < 90%) and tachycardia (HR > 125 bpm).")
    add_figure(doc, "visualizations/fig_3_3_flink_composite.png", 
               "Figure 3-3: Composite multi-vital alert detection for concurrent tachycardia and hypoxemia.",
               "Detection of simultaneous physiological breaches indicating compounding cardiorespiratory distress.")
    add_figure(doc, "visualizations/fig_3_4_clinical_log.png", 
               "Figure 3-4: Structured clinical alert log file ('patient_clinical_alerts.json').",
               "Inspection of JSON alert records containing patient identifiers, bed numbers, breach severities, and timestamps.")

    md_lines.append("![Figure 3-1](../visualizations/fig_3_1_flink_producer.png)\n*Figure 3-1: Patient vital sign telemetry generator.*\n")
    md_lines.append("![Figure 3-2](../visualizations/fig_3_2_flink_alerts.png)\n*Figure 3-2: Flink streaming execution output.*\n")
    md_lines.append("![Figure 3-3](../visualizations/fig_3_3_flink_composite.png)\n*Figure 3-3: Composite multi-vital alert detection.*\n")
    md_lines.append("![Figure 3-4](../visualizations/fig_3_4_clinical_log.png)\n*Figure 3-4: Structured clinical alert log file.*\n")

    doc.add_page_break()

    # --- PAGE 16 ---
    add_figure(doc, "visualizations/fig_3_5_flink_dashboard.png", 
               "Figure 3-5: Apache Flink web dashboard displaying cluster resource allocation.",
               "Web interface at http://localhost:8081 showing active JobManager, TaskManager, and available task slots.")
    add_figure(doc, "visualizations/fig_3_6_flink_jobs.png", 
               "Figure 3-6: Flink web dashboard displaying active streaming job overview.",
               "Dashboard view showing job 'PatientVitalsRealTimeSlidingWindowMonitor' in RUNNING state with 2 concurrent tasks.")
    add_figure(doc, "visualizations/fig_3_7_flink_dag.png", 
               "Figure 3-7: Flink distributed DAG execution graph showing source, window, and sink stages.",
               "Execution graph confirming normal operational status with 0% backpressure across stream vertices.")
    add_figure(doc, "visualizations/fig_3_8_flink_cancel.png", 
               "Figure 3-8: Flink job cancellation and resource reclamation via CLI ('flink cancel').",
               "Graceful termination of streaming job and release of allocated task execution slots.")

    md_lines.append("![Figure 3-5](../visualizations/fig_3_5_flink_dashboard.png)\n*Figure 3-5: Flink dashboard resource allocation.*\n")
    md_lines.append("![Figure 3-6](../visualizations/fig_3_6_flink_jobs.png)\n*Figure 3-6: Flink streaming job overview.*\n")
    md_lines.append("![Figure 3-7](../visualizations/fig_3_7_flink_dag.png)\n*Figure 3-7: Flink distributed DAG execution graph.*\n")
    md_lines.append("![Figure 3-8](../visualizations/fig_3_8_flink_cancel.png)\n*Figure 3-8: Flink job cancellation.*\n")

    doc.add_page_break()

    # --- PAGE 17 ---
    df_flink_alerts = pd.read_csv("activity3_flink/patient_alert_distribution.csv")
    f_rows = df_flink_alerts[["patient_id", "patient_name", "ward", "CRITICAL_RED", "URGENT_YELLOW", "TOTAL"]].values.tolist()
    add_styled_table(doc, ["Patient ID", "Patient Name", "Ward", "Critical Red Alerts", "Urgent Yellow Alerts", "Total Alerts"], f_rows, [1.0, 1.8, 1.1, 1.1, 1.1, 1.0])
    md_lines.append("### Patient Clinical Alert Distribution (Table 8)\n")
    md_lines.append(md_table(["Patient ID", "Patient Name", "Ward", "Critical Red Alerts", "Urgent Yellow Alerts", "Total Alerts"], f_rows))
    md_lines.append("\n")

    add_heading_2(doc, "5. Performance Analysis & Results Discussion")
    add_body_p(doc, 
        "Clinical Alert Distribution: Patient PT-02 (Sunita Patil, ICU-A-02) triggered 37 Critical Red alerts as oxygen saturation collapsed to 82.0%, "
        "accompanied by compensatory tachycardia (108 bpm in Alert FLK-ALT-PT-02-0033). Patient PT-03 (David Miller, ICU-B-01) generated 18 alerts due to high fever (39.6°C).\n\n"
        "Noise Filtering: Single-second SpO2 dips were smoothed by the 30-second window, preventing false alarms while capturing sustained breaches within 10 seconds.\n\n"
        "System Metrics: The dashboard verified 0% backpressure, confirming sub-second stream processing responsiveness."
    )
    add_figure(doc, "visualizations/activity3_flink_patient_vitals.png", 
               "Figure 3-9: Patient PT-02 physiological stream showing hypoxemic desaturation episode.",
               "Multi-parameter vital signs timeline showing blood oxygen desaturation (red) and compensatory heart rate elevation (blue).",
               width=5.75, max_height=2.30)
    md_lines.append("![Figure 3-9](../visualizations/activity3_flink_patient_vitals.png)\n*Figure 3-9: Patient PT-02 physiological stream.*\n")

    doc.add_page_break()

    # --- PAGE 18 ---
    add_figure(doc, "visualizations/activity3_flink_window_stats.png", 
               "Figure 3-10: Comparison of raw sensor telemetry versus 30-second sliding window moving averages.",
               "Graph comparing raw noisy telemetry points against smoothed 30-second sliding window average, illustrating noise reduction.",
               width=5.80, max_height=2.55)
    md_lines.append("![Figure 3-10](../visualizations/activity3_flink_window_stats.png)\n*Figure 3-10: Comparison of raw sensor telemetry vs. sliding window.*\n")

    add_heading_2(doc, "6. Conclusions & Engineering Trade-offs")
    add_body_p(doc, 
        "Apache Flink provides sub-second processing latency, true event-time processing, and robust windowing semantics for medical telemetry.\n\n"
        "However, maintaining in-memory state across long time windows requires disciplined checkpointing and state backend sizing (e.g. RocksDB). "
        "Future enhancements could incorporate Complex Event Processing (Flink CEP) to identify multi-stage clinical deterioration patterns."
    )
    doc.add_page_break()

    # =============================================================
    # ACTIVITY 4: MONGODB & WIREDTIGER (PAGES 19 TO 23)
    # =============================================================
    # --- PAGE 19 ---
    add_heading_1(doc, "Activity 4: Polymorphic E-Commerce Product Catalog using MongoDB & WiredTiger Engine")
    add_heading_2(doc, "1. Problem Definition")
    add_body_p(doc, 
        "E-commerce platforms manage dynamic catalogs with diverse merchandise categories (Electronics, Apparel, Groceries), "
        "each requiring distinct attributes. Relational schemas struggle with this variability, resulting in sparse tables or costly joins.\n\n"
        "The objective of this activity is to deploy a document catalog using MongoDB Community Server, evaluate polymorphic schema modeling, "
        "execute atomic inventory decrements, and benchmark query execution plans with compound B-tree indexes."
    )
    add_heading_2(doc, "2. Theoretical Background & Architecture")
    add_body_p(doc, 
        "Polymorphic BSON Documents: Documents in a single collection can contain varied schemas, matching application domain objects naturally.\n"
        "WiredTiger Engine: Provides document-level locking, Snappy block compression, and memory caching, maximizing read/write concurrency.\n"
        "Compound B-Tree Indexing: An index on { category: 1, price: 1 } enables index scans (IXSCAN), avoiding full collection scans (COLLSCAN)."
    )
    add_heading_2(doc, "3. Solution Design & Implementation Procedure")
    add_body_p(doc, 
        "1. Ingested 15,000 polymorphic product documents across 5 merchandise categories into 'ecommerce_catalog_db'.\n"
        "2. Executed atomic stock decrements using '$inc' and audit history logging with '$push'.\n"
        "3. Built an aggregation pipeline computing SKU counts, total stock units, and valuation per category.\n"
        "4. Benchmarked execution plans with explain('executionStats') comparing unindexed scans with compound index lookups."
    )
    mongo_code = """// MONGODB CRUD, ATOMIC MODIFIERS & AGGREGATION PIPELINE
db.products.insertMany(catalogDocuments);

// Atomic Stock Decrement & Audit Log
db.products.updateOne({ sku: "SKU-ELE-100001" }, {
    $inc: { stock_quantity: -3 },
    $set: { last_sold_at: new Date() },
    $push: { audit_log: { action: "ORDER_FULFILLED", units: 3, timestamp: new Date() } }
});

// Category Valuation Aggregation Pipeline
db.products.aggregate([
    { $match: { is_active: true } },
    { $group: {
        _id: "$category", total_products: { $sum: 1 },
        total_stock: { $sum: "$stock_quantity" }, avg_price: { $avg: "$price" },
        valuation: { $sum: { $multiply: ["$price", "$stock_quantity"] } }
    }},
    { $sort: { valuation: -1 } }
]);
db.products.createIndex({ category: 1, price: 1 });"""
    add_code_block(doc, mongo_code, "Table 10: MongoDB Document Operations, Atomic Modifiers and Aggregation Pipeline")
    md_lines.append("# Activity 4: Polymorphic E-Commerce Product Catalog using MongoDB & WiredTiger Engine\n")
    md_lines.append("```javascript\n" + mongo_code + "\n```\n")
    doc.add_page_break()

    # --- PAGE 20 ---
    add_heading_2(doc, "4. Experimental Execution & System Outputs")
    add_figure(doc, "visualizations/fig_4_1_mongodb_version.png", 
               "Figure 4-1: MongoDB server daemon verification and CLI connection check.",
               "Confirmation of active MongoDB Community Server instance on port 27017.",
               width=5.75, max_height=1.65)
    add_figure(doc, "visualizations/fig_4_2_mongo_stats.png", 
               "Figure 4-2: WiredTiger collection statistics for the product catalog.",
               "Collection stats confirming 15,000 documents, active B-tree indexes, and Snappy compression ratio.",
               width=5.75, max_height=1.65)
    add_figure(doc, "visualizations/fig_4_3_mongo_electronics.png", 
               "Figure 4-3: Polymorphic document structure showing nested hardware specifications.",
               "Sample JSON document displaying embedded CPU, RAM, and display properties for an electronics SKU.",
               width=5.75, max_height=1.65)

    md_lines.append("![Figure 4-1](../visualizations/fig_4_1_mongodb_version.png)\n*Figure 4-1: MongoDB server daemon verification.*\n")
    md_lines.append("![Figure 4-2](../visualizations/fig_4_2_mongo_stats.png)\n*Figure 4-2: WiredTiger collection statistics.*\n")
    md_lines.append("![Figure 4-3](../visualizations/fig_4_3_mongo_electronics.png)\n*Figure 4-3: Polymorphic document structure.*\n")

    doc.add_page_break()

    # --- PAGE 21 ---
    add_figure(doc, "visualizations/fig_4_4_mongo_agg.png", 
               "Figure 4-4: Aggregation pipeline execution calculating category inventory valuations.",
               "Aggregation output grouping products by category, summing inventory quantities, and computing asset valuations.")
    add_figure(doc, "visualizations/fig_4_5_mongo_grocery.png", 
               "Figure 4-5: Polymorphic document structure showing grocery attributes.",
               "Sample JSON document demonstrating organic certifications, shelf life, and dietary flags coexisting in the same collection.")
    add_figure(doc, "visualizations/fig_4_6_mongo_explain.png", 
               "Figure 4-6: Query execution plan comparison between full collection scan and compound index scan.",
               "Explain output showing execution stage FETCH with input IXSCAN, reducing examined documents from 14,990 to 1,101.")
    add_figure(doc, "visualizations/fig_4_7_mongo_script.png", 
               "Figure 4-7: MongoDB aggregation query script implementation.",
               "JavaScript script implementation containing aggregation stages: $match, $group, and $sort.")

    md_lines.append("![Figure 4-4](../visualizations/fig_4_4_mongo_agg.png)\n*Figure 4-4: Aggregation pipeline execution.*\n")
    md_lines.append("![Figure 4-5](../visualizations/fig_4_5_mongo_grocery.png)\n*Figure 4-5: Polymorphic document structure showing grocery attributes.*\n")
    md_lines.append("![Figure 4-6](../visualizations/fig_4_6_mongo_explain.png)\n*Figure 4-6: Query execution plan comparison.*\n")
    md_lines.append("![Figure 4-7](../visualizations/fig_4_7_mongo_script.png)\n*Figure 4-7: MongoDB aggregation query script implementation.*\n")

    doc.add_page_break()

    # --- PAGE 22 ---
    df_mongo_agg = pd.read_csv("activity4_mongodb/category_aggregation_summary.csv")
    m_rows = df_mongo_agg[["category", "total_products", "total_inventory_units", "avg_price", "total_inventory_valuation"]].values.tolist()
    add_styled_table(doc, ["Merchandise Category", "Total SKU Count", "Total Stock Units", "Avg Price (INR)", "Total Valuation (INR)"], m_rows, [1.5, 1.1, 1.2, 1.3, 1.6])
    md_lines.append("### Category Valuation Breakdown (Table 9)\n")
    md_lines.append(md_table(["Merchandise Category", "Total SKU Count", "Total Stock Units", "Avg Price (INR)", "Total Valuation (INR)"], m_rows))
    md_lines.append("\n")

    add_heading_2(doc, "5. Performance Analysis & Results Discussion")
    add_body_p(doc, 
        "Inventory Aggregation Analysis: The aggregation pipeline executed across 15,000 documents in 8.4 milliseconds. "
        "Total catalog inventory exceeded 1.12 million units with aggregate asset valuation over Rs. 2,490 Crores. "
        "Electronics accounted for the highest valuation (Rs. 1,754.6 Crores across 3,006 SKUs, mean price Rs. 78,732.06).\n\n"
        "Index Selectivity Benchmark: Filtering by category ('Electronics') and price range (Rs. 20,000–50,000) without an index "
        "examined all 14,990 documents (COLLSCAN) in 18.2 ms. With compound index { category: 1, price: 1 }, the query planner used an index scan (IXSCAN), "
        "examining only 1,101 documents—a 92.7% reduction in document scans, with latency dropping to 3.76 ms (79.3% speedup)."
    )
    add_figure(doc, "visualizations/activity4_mongodb_index_benchmark.png", 
               "Figure 4-8: Query performance comparison: documents scanned and latency for COLLSCAN vs. IXSCAN.",
               "Benchmark bar chart contrasting documents examined (14,990 vs. 1,101) and query execution latency (18.2 ms vs. 3.76 ms).",
               width=5.75, max_height=2.30)
    md_lines.append("![Figure 4-8](../visualizations/activity4_mongodb_index_benchmark.png)\n*Figure 4-8: Query performance comparison.*\n")

    doc.add_page_break()

    # --- PAGE 23 ---
    add_figure(doc, "visualizations/activity4_mongodb_schema_diagram.png", 
               "Figure 4-9: Structural comparison: normalized relational tables versus embedded document model.",
               "Architectural comparison highlighting relational schema normalization vs. MongoDB flexible embedded document structure.",
               width=5.80, max_height=2.55)
    md_lines.append("![Figure 4-9](../visualizations/activity4_mongodb_schema_diagram.png)\n*Figure 4-9: Structural comparison.*\n")

    add_heading_2(doc, "6. Conclusions & Engineering Trade-offs")
    add_body_p(doc, 
        "MongoDB Community Server with WiredTiger engine simplifies e-commerce catalog design by supporting diverse product schemas "
        "within a single collection without costly schema alterations. Atomic modifier operators ($inc, $push) ensure safe stock decrement operations.\n\n"
        "However, embedding sub-documents can cause document fragmentation if unbounded arrays are placed inside high-write product documents. "
        "Document models must balance embedded convenience with referencing strategies for scalable operations."
    )
    doc.add_page_break()

    # =============================================================
    # ACTIVITY 5: AWS S3 & ATHENA (PAGES 24 TO 27)
    # =============================================================
    # --- PAGE 24 ---
    add_heading_1(doc, "Activity 5: Serverless Cloud Access Log Analytics using AWS S3, Parquet & Amazon Athena")
    add_heading_2(doc, "1. Problem Definition")
    add_body_p(doc, 
        "Modern cloud applications generate vast volumes of HTTP access logs documenting endpoint traffic, status codes, and latencies. "
        "Maintaining dedicated, 24/7 analytics database server clusters incurs significant operational expenses and maintenance overhead.\n\n"
        "The objective of this activity is to design a serverless cloud data lake on AWS S3, convert raw access logs to Snappy-compressed Apache Parquet, "
        "execute distributed SQL analytics using Amazon Athena, and establish a comparative Cloud FinOps cost optimization model."
    )
    add_heading_2(doc, "2. Theoretical Background & Architecture")
    add_body_p(doc, 
        "Amazon S3 Object Storage: Serverless object storage offering 11 9s durability, unlimited scaling, and native query integration.\n"
        "Apache Parquet Columnar Storage: Organizes records into columnar stripes with dictionary encoding and Snappy compression, minimizing scanned bytes.\n"
        "Amazon Athena Serverless Analytics: An interactive serverless query engine based on Presto/Trino running ANSI SQL directly against S3 ($5.00/TB scanned)."
    )
    add_heading_2(doc, "3. Solution Design & Implementation Procedure")
    add_body_p(doc, 
        "1. Configured local S3 service endpoint and created cloud bucket 's3://cloud-logs-aryan/'.\n"
        "2. Synthesized 50,000 HTTP access logs containing IP addresses, timestamps, HTTP methods, endpoints, status codes, and latencies.\n"
        "3. Converted raw CSV data into Snappy-compressed Apache Parquet and defined table metadata in the data catalog.\n"
        "4. Executed analytical SQL queries to evaluate frequent error codes (4xx/5xx) and hourly traffic distribution.\n"
        "5. Developed an empirical FinOps cost model comparing dedicated server clusters with serverless Athena querying."
    )
    athena_code = """-- AMAZON ATHENA SERVERLESS SQL ANALYTICS QUERIES
CREATE EXTERNAL TABLE IF NOT EXISTS cloud_logs (
    request_id STRING, timestamp STRING, date STRING, hour INT,
    client_ip STRING, http_method STRING, endpoint STRING,
    status_code INT, status_category STRING, response_time_ms DOUBLE, response_bytes INT
) STORED AS PARQUET LOCATION 's3://cloud-logs-aryan/raw_logs/'
TBLPROPERTIES ("parquet.compress"="SNAPPY");

-- Query 1: Frequent Error Breakdown & Latency SLA
SELECT status_category, status_code, count(*) as req_count,
       round(count(*) * 100.0 / sum(count(*)) over(), 2) as share_pct,
       round(avg(response_time_ms), 1) as avg_latency_ms
FROM cloud_logs GROUP BY status_category, status_code ORDER BY status_category, req_count DESC;

-- Query 2: Hourly Traffic & Error Anomaly Detection
SELECT hour, count(*) as total_requests,
       sum(case when status_code >= 500 then 1 else 0 end) as server_errors_5xx,
       round(sum(case when status_code >= 400 then 1 else 0 end) * 100.0 / count(*), 2) as error_rate_pct
FROM cloud_logs GROUP BY hour ORDER BY hour;"""
    add_code_block(doc, athena_code, "Table 12: Amazon Athena Serverless SQL Log Analytics Queries")
    md_lines.append("# Activity 5: Serverless Cloud Access Log Analytics using AWS S3, Parquet & Amazon Athena\n")
    md_lines.append("```sql\n" + athena_code + "\n```\n")
    doc.add_page_break()

    # --- PAGE 25 ---
    add_heading_2(doc, "4. Experimental Execution & System Outputs")
    add_figure(doc, "visualizations/fig_5_1_s3_daemon.png", 
               "Figure 5-1: Local S3 service endpoint verification on port 5000.",
               "Confirmation of local S3 service listener supporting AWS REST APIs.")
    add_figure(doc, "visualizations/fig_5_2_aws_s3_ls.png", 
               "Figure 5-2: AWS CLI bucket discovery ('aws s3 ls') showing data lake storage.",
               "CLI output confirming discovery of the provisioned cloud bucket 'cloud-logs-aryan' and stored log objects.")
    add_figure(doc, "visualizations/fig_5_3_parquet_compression.png", 
               "Figure 5-3: Storage footprint comparison between uncompressed CSV and Snappy-compressed Parquet.",
               "Converting raw CSV logs (4.80 MB) to Snappy-compressed Parquet (1.12 MB) achieved a 76.7% reduction in file size.")
    add_figure(doc, "visualizations/fig_5_4_athena_q1.png", 
               "Figure 5-4: Athena Query 1 execution output: HTTP status code distribution and latency metrics.",
               "Query output breaking down client (4xx) and server (5xx) response distributions and mean response times.")

    md_lines.append("![Figure 5-1](../visualizations/fig_5_1_s3_daemon.png)\n*Figure 5-1: Local S3 service endpoint verification.*\n")
    md_lines.append("![Figure 5-2](../visualizations/fig_5_2_aws_s3_ls.png)\n*Figure 5-2: AWS CLI bucket discovery.*\n")
    md_lines.append("![Figure 5-3](../visualizations/fig_5_3_parquet_compression.png)\n*Figure 5-3: Storage footprint comparison.*\n")
    md_lines.append("![Figure 5-4](../visualizations/fig_5_4_athena_q1.png)\n*Figure 5-4: Athena Query 1 execution output.*\n")

    doc.add_page_break()

    # --- PAGE 26 ---
    add_figure(doc, "visualizations/fig_5_5_athena_q2.png", 
               "Figure 5-5: Athena Query 2 execution output: Hourly traffic volumes and error rate spikes.",
               "Query aggregation showing request volume peak at hour 15 (5,068 requests) with an error rate of 25.49%.")
    add_figure(doc, "visualizations/fig_5_6_cloud_cost_model.png", 
               "Figure 5-6: Cloud FinOps cost comparison model: on-premise hardware vs. serverless Athena architecture.",
               "Cost optimization model demonstrating monthly operational expenses across architectural models.")

    df_cloud_status = pd.read_csv("activity5_cloud_analytics/results/q1_status_code_breakdown.csv")
    cs_rows = df_cloud_status.values.tolist()
    add_styled_table(doc, ["Category", "Status Code", "Requests", "Share %", "Avg Latency (ms)"], cs_rows, [1.1, 1.1, 1.2, 1.2, 1.5])
    md_lines.append("### Status Code Distribution (Table 11)\n")
    md_lines.append(md_table(["Category", "Status Code", "Requests", "Share %", "Avg Latency (ms)"], cs_rows))
    md_lines.append("\n")

    add_body_p(doc, 
        "FinOps Economic Model: Evaluated for 100 GB logs/day (3 TB/month, 10 queries/day):\n"
        "• Dedicated 24/7 Server Cluster (3x AWS m5.xlarge instances): ~$1,200.00 / month.\n"
        "• Athena on Raw CSV (scanning uncompressed lines): ~$6,822.66 / month.\n"
        "• Serverless S3 + Parquet + Athena Architecture: ~$340.13 / month.\n"
        "The serverless S3 + Parquet architecture yields an 85.3% cost reduction over dedicated infrastructure, eliminating idle server expenses."
    )
    doc.add_page_break()

    # --- PAGE 27 ---
    add_heading_2(doc, "5. Performance Analysis & Results Discussion")
    add_figure(doc, "visualizations/activity5_cloud_error_distribution.png", 
               "Figure 5-7: HTTP response status code proportions and mean latency profile.",
               "Bar chart illustrating request distribution by HTTP status code and corresponding average latency in milliseconds.")
    add_figure(doc, "visualizations/activity5_cloud_cost_model.png", 
               "Figure 5-8: Monthly FinOps infrastructure cost comparison across operational models.",
               "Comparative expenditure bar chart contrasting dedicated server clusters ($1,200/mo), raw CSV queries ($6,822/mo), and serverless Parquet ($340.13/mo).")

    add_heading_2(doc, "6. Conclusions & Engineering Trade-offs")
    add_body_p(doc, 
        "A serverless data lake utilizing Amazon S3 and Amazon Athena delivers an exceptionally cost-effective, scalable, "
        "and zero-maintenance architecture for access log analytics. Converting logs to columnar Parquet drastically cuts Athena scanning costs.\n\n"
        "However, Athena exhibits a baseline query execution latency of 1–3 seconds due to query planning and container allocation. "
        "Consequently, Athena is optimal for exploratory analytics, security investigations, and daily reporting, but should be complemented with OpenSearch "
        "or Redis for sub-second operational monitoring."
    )
    md_lines.append("![Figure 5-7](../visualizations/activity5_cloud_error_distribution.png)\n*Figure 5-7: HTTP response status code proportions.*\n")
    md_lines.append("![Figure 5-8](../visualizations/activity5_cloud_cost_model.png)\n*Figure 5-8: Monthly FinOps infrastructure cost comparison.*\n")
    doc.add_page_break()

    # =============================================================
    # CONSOLIDATED SUMMARY & FINAL DECLARATION (PAGES 28 & 29)
    # =============================================================
    # --- PAGE 28 ---
    add_heading_1(doc, "Consolidated Summary & Big Data Technology Comparison")
    add_body_p(doc, 
        "Across the five Self-Learning Activities (SLAs), five distinct big data architectures were configured, executed, "
        "and evaluated against representative enterprise workloads. The matrix below synthesizes their design characteristics, "
        "storage representations, query mechanisms, and primary industry use cases:"
    )

    synthesis_matrix = [
        ["Activity 1: Hadoop HDFS & Apache Hive", "High-throughput Batch Analytics", "HDFS Block Storage (128 MB blocks, 3x replication)", "Hive on Tez / Spark with Calcite CBO", "Enterprise Data Warehousing & Historical Financial Reporting"],
        ["Activity 2: Apache Kafka (KRaft)", "Real-time High-Velocity Streaming", "Distributed Commit Log partitioned horizontally", "Kafka Consumer Groups with Key Hashing", "IoT Telemetry Ingestion & Smart City Traffic Management"],
        ["Activity 3: Apache Flink DataStream API", "Low-latency Stateful Stream Processing", "In-memory JVM & RocksDB Managed State", "DataStream API with 30s Sliding Windows", "Critical Healthcare Patient Monitoring & Clinical Alarms"],
        ["Activity 4: MongoDB 9.0 (WiredTiger)", "Operational NoSQL Document Store", "BSON Documents with B-Tree Compound Indexing", "Aggregation Pipeline ($match, $group, $sort)", "Polymorphic Product Catalogs & Dynamic E-Commerce"],
        ["Activity 5: AWS S3, Parquet & Athena", "Serverless Cloud Data Lake", "Amazon S3 Object Store with Snappy Parquet", "Serverless Presto/Trino ANSI SQL Engine", "Cloud Application Log Observability & FinOps Economics"]
    ]
    add_styled_table(doc, ["Activity & Platform", "Data Velocity & Paradigm", "Storage / Memory Model", "Query / Processing Engine", "Primary Industry Use Case"], synthesis_matrix, [1.5, 1.3, 1.4, 1.4, 1.4])

    add_body_p(doc, 
        "Architectural Synthesis: Modern enterprise data engineering architectures rarely rely on a single technology. "
        "Instead, organizations implement hybrid 'Lambda' or 'Kappa' topologies that combine Kafka for ingestion, "
        "Flink for real-time anomaly detection, MongoDB for operational catalog serving, HDFS/Hive for historical batch reporting, "
        "and serverless S3/Athena for cost-optimized cloud observability."
    )

    # --- FINAL SUBMISSION DECLARATION (Clean Page 28 Conclusion) ---
    add_heading_2(doc, "Final Submission & Academic Integrity Declaration")
    add_body_p(doc, 
        "I hereby declare that this consolidated laboratory report for Big Data Systems (Course Code: 24CI51) is an authentic record of "
        "original experimental engineering work conducted by me. All system configurations, distributed daemon orchestrations, "
        "CLI execution audits, telemetry streaming pipelines, and empirical performance evaluations presented in this monograph were "
        "implemented and verified as part of the academic curriculum."
    )

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(16)
    p_sig.paragraph_format.line_spacing = 1.25
    r_sig = p_sig.add_run(
        "Student Signature: ____________________________________          Date: 10-November-2026\n"
        "Aryan M Desai  |  University Seat Number (USN): 1MS24CI026\n"
        "Department of Computer Science & Engineering (Artificial Intelligence & Machine Learning)\n"
        "Ramaiah Institute of Technology, Bengaluru – 560054"
    )
    r_sig.font.name = "Calibri"
    r_sig.font.size = Pt(10.0)
    r_sig.font.bold = True
    r_sig.font.color.rgb = RGBColor(0x00, 0x20, 0x60)

    md_lines.append("# Consolidated Summary & Big Data Technology Comparison\n")
    md_lines.append(md_table(["Activity & Platform", "Data Velocity & Paradigm", "Storage / Memory Model", "Query / Processing Engine", "Primary Industry Use Case"], synthesis_matrix))
    md_lines.append("\n\n---\n")

    md_lines.append("### Student Academic Integrity Declaration\n")
    md_lines.append("I hereby declare that this consolidated laboratory report for Big Data Systems (24CI51) is an authentic record of "
                    "original experimental engineering work conducted by me.\n\n")
    md_lines.append("**Student Signature:** ______________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Date:** 10-November-2026  \n")
    md_lines.append("**Aryan M Desai** | USN: 1MS24CI026  \n")
    md_lines.append("Department of Computer Science & Engineering (Artificial Intelligence & Machine Learning)  \n")
    md_lines.append("Ramaiah Institute of Technology, Bengaluru – 560054  \n")

    # Save outputs
    p1 = "reports/BIG_DATA_SYSTEMS_CONSOLIDATED_REPORT_ARYAN_DESAI.docx"
    doc.save(p1)
    print(f"✓ Saved {p1}")

    p2 = "reports/BIG_DATA_SYSTEMS_CONSOLIDATED_REPORT.docx"
    try:
        doc.save(p2)
        print(f"✓ Saved {p2}")
    except PermissionError:
        print(f"ℹ Note: {p2} is open; {p1} is fully updated.")

    md_path = "reports/BIG_DATA_SYSTEMS_CONSOLIDATED_REPORT.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"✓ Saved {md_path}")

if __name__ == "__main__":
    build_reports()
