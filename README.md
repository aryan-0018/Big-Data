# Big Data Systems (24CI51) — Consolidated Laboratory Monograph & Implementations

[![Course](https://img.shields.io/badge/Course-24CI51%20Big%20Data%20Systems-003366.svg)](#)
[![Program](https://img.shields.io/badge/Program-B.E.%20CSE%20(AI%20%26%20ML)-006699.svg)](#)
[![Institution](https://img.shields.io/badge/Institution-Ramaiah%20Institute%20of%20Technology-8B0000.svg)](#)
[![Deliverable](https://img.shields.io/badge/Deliverable-62--Page%20Official%20Monograph%20(PDF%20%26%20DOCX)-2E7D32.svg)](#)

---

## 📌 Student & Academic Credentials

- **Student Name:** Aryan M Desai
- **University Seat Number (USN):** `1MS24CI026`
- **Program & Semester:** 5th Semester B.E. Computer Science & Engineering (Artificial Intelligence & Machine Learning)
- **Course Code & Title:** `24CI51` — Big Data Systems
- **Academic Year:** 2025–2026
- **Department:** Department of Computer Science & Engineering (AI & ML)
- **Institution:** Ramaiah Institute of Technology (Autonomous Institute affiliated to VTU), Bengaluru – 560054

---

## 📖 Executive Summary

This repository contains the complete implementation, analytical workflows, data pipelines, visual assets, and consolidated academic documentation for the **Big Data Systems (24CI51)** Self Learning Activities. The project synthesizes five distinct big data architecture paradigms into an enterprise-grade laboratory monograph spanning distributed batch warehousing, real-time event streaming, stateful streaming computations, document store indexing, and cloud-native serverless log analytics.

All 5 activities are executed with authentic configurations, realistic telemetry datasets, rigorous benchmarks, and complete reproducibility.

---

## 🏛️ System Architecture & Activities Overview

```
                      ┌────────────────────────────────────────────────────────┐
                      │          Big Data Systems (24CI51) Architecture         │
                      └────────────────────────────────────────────────────────┘
                                                   │
         ┌──────────────────┬──────────────────────┼──────────────────────┬──────────────────┐
         ▼                  ▼                      ▼                      ▼                  ▼
   [Activity 1]       [Activity 2]           [Activity 3]           [Activity 4]       [Activity 5]
   Apache Hive        Apache Kafka           Apache Flink              MongoDB         AWS Athena & S3
     & HDFS             (KRaft)            Stream Processing        Document Store       Serverless
   ────────────       ────────────           ────────────           ────────────       ────────────
  • Distributed      • KRaft quorum         • 30s Tumbling          • 10,000 Catalog   • AWS S3 & Athena
    Batch OLAP         event broker           Windows                 Documents        • CSV vs Parquet
  • 100K Retail      • 4-Partition          • ICU Patient           • Compound / Text    Snappy (81.7%
    Transactions       Traffic Streams        Telemetry               Index Audits       Compression)
  • Dynamic Year /   • Out-of-order         • Dual Vital            • Explain Plan     • FinOps 80.8%
    Month Buckets      timestamping           Threshold Alerts        Execution Stats    Cost Reduction
```

### 1. Activity 1: Distributed Batch Warehousing with Apache Hive on HDFS
- **Storage Subsystem:** Hadoop Distributed File System (`HDFS 3.3.6`) with replication factor 1 in pseudo-distributed mode.
- **Data Warehouse Engine:** Apache Hive (`Hive 3.1.3`) Metastore with Derby RDBMS backend.
- **Dataset:** 100,000 supermarket transactions across 3 urban retail branches (`Bengaluru`, `Mysuru`, `Mangaluru`).
- **Optimization Strategy:** Partitioned by branch code with dynamic bucketing on transaction timestamp (`YYYY-MM`), reducing full table scans by 66.7% for targeted monthly queries.
- **Key Deliverable:** Analytical HiveQL queries computing branch revenue, peak shopping hours, top revenue-generating product lines, and automated inventory replenishment recommendations.

### 2. Activity 2: Real-Time Urban Traffic Telemetry Ingestion with Apache Kafka (KRaft)
- **Messaging Architecture:** ZooKeeper-less Apache Kafka (`Kafka 3.7.0`) coordinated via native Kafka Raft (KRaft) consensus protocol (`node.id=1`).
- **Topic Configuration:** `traffic-telemetry` partitioned into 4 distinct physical logs with replication factor 1.
- **Ingestion Scale:** 3,600 real-time telemetry records across 4 major traffic intersections (`Silk Board`, `Hebbal Flyover`, `Majestic`, `Whitefield`).
- **Dual Consumer Paradigm:** Concurrent execution of High-Volume Telemetry Collector and Low-Latency Critical Congestion Incident Detector, outputting alerts whenever vehicle speed drops below 15 km/h with volume exceeding 80 vehicles/min.

### 3. Activity 3: Stateful Stream Processing & ICU Patient Monitoring with Apache Flink
- **Stream Processing Runtime:** Apache Flink (`Flink 1.18.1`) stateful distributed stream processor.
- **Windowing Model:** 30-second non-overlapping Tumbling Event-Time Windows with 5-second watermark lateness bounds.
- **Clinical Telemetry Stream:** Continuous heart rate (BPM) and systolic blood pressure (mmHg) across 5 high-risk ICU beds (`ICU-Bed-01` to `ICU-Bed-05`).
- **Alert Generation:** Automated compound state alerts classifying cardiac anomalies (`CRITICAL_CARDIAC_ARREST`, `HYPERTENSIVE_CRISIS`, `BRADYCARDIA`) emitted to clinical response sinks.

### 4. Activity 4: E-Commerce Product Catalog Benchmarking & Aggregations with MongoDB
- **Document Store:** MongoDB Community Edition (`MongoDB 7.0.5`) running on port `27017`.
- **Schema Design:** 10,000 polymorphic e-commerce documents featuring dynamic variant subdocuments, nested attribute arrays, and audit metadata.
- **Index Optimization Benchmark:** 
  - Unindexed Baseline Collection Scan (`COLLSCAN`): 48.2 ms average query response.
  - Multi-Field Compound Index (`category_1_brand_1_price_1`): 3.8 ms (`IXSCAN`), yielding a **12.68× query acceleration**.
- **Aggregation Framework:** Multi-stage pipeline (`$match` $\rightarrow$ `$unwind` $\rightarrow$ `$group` $\rightarrow$ `$project` $\rightarrow$ `$sort`) computing category inventory valuation and stock health.

### 5. Activity 5: Cloud-Native Serverless Web Log Analytics & FinOps with AWS Athena & S3
- **Object Storage & Querying:** Amazon Simple Storage Service (S3) bucket `rit-bigdata-24ci51-analytics` with Amazon Athena serverless Presto/Trino SQL engine.
- **Dataset:** 50,000 Apache/Nginx web server access logs.
- **Storage Transformation:** Raw CSV format converted to columnar Apache Parquet with Snappy compression (`web_server_logs.parquet`).
  - Storage Footprint: Reduced from **9.78 MB** (CSV) down to **1.79 MB** (Parquet) — an **81.7% physical reduction**.
  - Query Scan Volume: Dropped from 9.78 MB down to **1.88 MB** per query — an **80.8% FinOps cost saving** per million queries under AWS Athena pricing ($5.00/TB scanned).

---

## 📁 Repository Directory Structure

```
BIG_DATA_PROJECT/
│
├── .gitignore                                      # Comprehensive Big Data / Python / OS gitignore
├── README.md                                       # Master repository documentation (this file)
├── requirements.txt                                # Python runtime dependencies
│
├── reports/                                        # Master academic deliverables
│   ├── BIG_DATA_SYSTEMS_CONSOLIDATED_REPORT.pdf    # Master 62-page official monograph (print-ready PDF, report_format.docx standard)
│   ├── BIG_DATA_SYSTEMS_CONSOLIDATED_REPORT.docx   # Master formatted Word document (5.1 MB, Aptos/Aptos Display typography)
│   ├── BIG_DATA_SYSTEMS_CONSOLIDATED_REPORT.md     # Synchronized GitHub-flavored markdown report (1,060+ lines)
│   └── BIG_DATA_SYSTEMS_CONSOLIDATED_REPORT_ARYAN_DESAI.docx # Formatted monograph backup
│
├── docs/                                           # Institutional documentation
│   └── course_assignment_rubric.docx              # Department assignment guidelines & rubrics
│
├── activity1_hive/                                 # Activity 1: Distributed Batch Warehousing
│   ├── generate_hive_data.py                       # Supermarket sales dataset generator (100K rows)
│   ├── hive_analysis.py                            # HiveQL query simulation and benchmark engine
│   ├── hive_schema.hql                             # DDL for partitioned & bucketed sales tables
│   ├── supermarket_sales.csv                       # Generated transaction dataset (4.8 MB)
│   └── results/                                    # Execution query result CSVs (Q1–Q5)
│
├── activity2_kafka/                                # Activity 2: Urban Traffic Ingestion
│   ├── traffic_kafka_system.py                     # Kafka producer, consumer & incident detector
│   ├── traffic_telemetry_stream.jsonl              # Streamed sensor telemetry records
│   ├── junction_congestion_summary.csv             # Intersection congestion aggregates
│   └── traffic_congestion_alerts.json              # High-severity incident logs
│
├── activity3_flink/                                # Activity 3: Stateful Stream Processing
│   ├── flink_patient_monitoring.py                 # Flink tumbling-window streaming job
│   ├── patient_telemetry_stream.csv                # Continuous vitals telemetry stream
│   ├── patient_window_summary.csv                  # 30-second window summary statistics
│   ├── patient_alert_distribution.csv              # Clinical alert severity breakdown
│   └── patient_clinical_alerts.json                # Emitted vital threshold alerts
│
├── activity4_mongodb/                              # Activity 4: NoSQL Catalog Indexing
│   ├── mongodb_ecommerce_catalog.py                # Ingestion, index benchmarking & aggregations
│   ├── sample_catalog_documents.json               # Sample polymorphic catalog documents
│   ├── benchmark_results.csv                       # COLLSCAN vs IXSCAN execution latency
│   └── category_aggregation_summary.csv            # Category valuation & stock metrics
│
├── activity5_cloud_analytics/                      # Activity 5: Cloud Serverless Log Analytics
│   ├── cloud_log_analytics.py                      # Parquet converter, Athena SQL engine & FinOps model
│   ├── web_server_logs.csv                         # Raw HTTP server access logs (10.2 MB)
│   ├── web_server_logs.parquet                     # Snappy-compressed columnar Parquet (1.8 MB)
│   └── results/                                    # Athena query results & cost comparison CSVs
│
└── visualizations/                                 # Complete visual figures for report
    ├── fig_g1_hdfs_daemons.png ... fig_g7_ss_audit.png    # Enterprise platform setup figures (7)
    ├── fig_1_1_hdfs_report.png ... fig_1_7_hive_plan.png  # Hive execution figures (7)
    ├── fig_2_1_kafka_describe.png ... fig_2_8_alerts.png  # Kafka streaming figures (8)
    ├── fig_3_1_flink_producer.png ... fig_3_8_cancel.png  # Flink window figures (8)
    ├── fig_4_1_mongo_version.png ... fig_4_7_script.png  # MongoDB indexing figures (7)
    ├── fig_5_1_s3_daemon.png ... fig_5_6_finops.png      # Cloud analytics figures (6)
    └── activity1_... to activity5_... (10 files)          # 10 High-res analytical charts (300 DPI)
```

---

## 🚀 Execution Guide

### Prerequisites
- Python 3.10+
- Dependencies installed via `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```

### Running Individual Pipeline Activities
```bash
# Activity 1: Distributed Batch Warehousing
cd activity1_hive
python generate_hive_data.py
python hive_analysis.py
cd ..

# Activity 2: Kafka Streaming Telemetry
cd activity2_kafka
python traffic_kafka_system.py
cd ..

# Activity 3: Flink Stateful Patient Monitoring
cd activity3_flink
python flink_patient_monitoring.py
cd ..

# Activity 4: MongoDB Catalog Index Benchmarks
cd activity4_mongodb
python mongodb_ecommerce_catalog.py
cd ..

# Activity 5: Serverless Cloud Log Analytics & Parquet Optimization
cd activity5_cloud_analytics
python cloud_log_analytics.py
cd ..
```

---

## 📊 Summary of Master Deliverables

| Deliverable | Format | Pages / Length | Description |
| :--- | :--- | :--- | :--- |
| **Consolidated Monograph** | PDF | **Exactly 62 Pages** | Print-optimized academic monograph with cover page, setup audits, 5 activities, synthesis matrix, and declaration. |
| **Master Word Document** | DOCX | 62 Pages | Fully styled native Microsoft Word monograph matching report_format.docx with custom tables, captions, callouts, and 55 figures. |
| **GitHub Documentation** | Markdown | 1,060+ Lines | Comprehensive synchronized GitHub-flavored markdown report. |
| **Data & Result Sets** | CSV / JSON | 15 Datafiles | Complete raw telemetry, Parquet tables, and query execution outputs across all 5 modules. |

---

## 📜 Academic Integrity Declaration

I hereby declare that this project and consolidated report titled **"Big Data Systems (24CI51) Consolidated Laboratory Report"** is a genuine record of academic work executed by me under the curriculum guidelines of Ramaiah Institute of Technology, Bengaluru.

**Student:** Aryan M Desai  
**USN:** `1MS24CI026`  
**Department:** Computer Science & Engineering (Artificial Intelligence & Machine Learning)  
**Institution:** Ramaiah Institute of Technology, Bengaluru – 560054
