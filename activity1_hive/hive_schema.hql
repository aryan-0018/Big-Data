
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
