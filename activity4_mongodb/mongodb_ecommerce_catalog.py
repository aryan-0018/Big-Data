"""
Enterprise E-Commerce Dynamic Product Catalog Engine using MongoDB NoSQL Database.
Demonstrates dynamic BSON schemas, CRUD operations, atomic modifiers,
aggregation pipelines, compound indexing, and explain() query execution plan benchmarks.
"""

import os
import json
import time
import random
from datetime import datetime
import pymongo
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 11})

os.makedirs("activity4_mongodb", exist_ok=True)
os.makedirs("visualizations", exist_ok=True)

def generate_catalog_documents(num_products=15000):
    """Generates heterogeneous e-commerce product catalog with category-specific nested attributes."""
    random.seed(42)
    categories = ["Electronics", "Apparel", "Home Appliances", "Books", "Groceries"]
    brands = {
        "Electronics": ["Apple", "Samsung", "Sony", "Dell", "HP", "Asus", "OnePlus", "Lenovo"],
        "Apparel": ["Nike", "Adidas", "Zara", "Levi's", "Puma", "Uniqlo", "H&M", "Under Armour"],
        "Home Appliances": ["LG", "Whirlpool", "Bosch", "Philips", "Dyson", "Panasonic", "Havells"],
        "Books": ["Penguin", "HarperCollins", "O'Reilly", "Routledge", "Pearson", "Bloomsbury"],
        "Groceries": ["Nestle", "Amul", "Tata Consumer", "Kellogg's", "Nature's Basket", "Organic India"]
    }

    products = []
    for i in range(1, num_products + 1):
        cat = random.choice(categories)
        brand = random.choice(brands[cat])
        sku = f"SKU-{cat[:3].upper()}-{100000 + i}"
        
        # Base product schema
        base = {
            "sku": sku,
            "category": cat,
            "brand": brand,
            "is_active": True,
            "is_discontinued": False,
            "created_at": datetime(2025, random.randint(1, 10), random.randint(1, 28)),
            "rating": {
                "average": round(random.uniform(3.2, 4.9), 1),
                "review_count": random.randint(5, 4500)
            },
            "stock_quantity": random.randint(0, 150),
            "warehouse_location": random.choice(["WH-BOM-01", "WH-BLR-02", "WH-DEL-01", "WH-HYD-03"]),
            "tags": []
        }

        # Category-specific polymorphic specifications
        if cat == "Electronics":
            sub = random.choice(["Laptop", "Smartphone", "Headphones", "Tablet", "Smartwatch"])
            price = round(random.uniform(12000, 145000), 2)
            base.update({
                "title": f"{brand} {sub} Pro {random.randint(11, 16)}",
                "sub_category": sub,
                "price": price,
                "cost_price": round(price * 0.78, 2),
                "specifications": {
                    "processor": random.choice(["Intel Core i7", "Apple M3", "Snapdragon 8 Gen 3", "Ryzen 7"]),
                    "ram_gb": random.choice([8, 16, 24, 32]),
                    "storage_gb": random.choice([256, 512, 1024]),
                    "battery_capacity_mah": random.choice([4500, 5000, 6000, 75000]),
                    "screen_size_inches": random.choice([6.1, 6.7, 13.3, 14.0, 16.0]),
                    "warranty_months": random.choice([12, 24, 36])
                },
                "tags": [sub.lower(), brand.lower(), "gadgets", "5g", "electronics"]
            })
        elif cat == "Apparel":
            sub = random.choice(["Running Shoes", "Denim Jacket", "Cotton T-Shirt", "Hoodie", "Athletic Shorts"])
            price = round(random.uniform(799, 9999), 2)
            base.update({
                "title": f"{brand} {sub} Edition",
                "sub_category": sub,
                "price": price,
                "cost_price": round(price * 0.55, 2),
                "specifications": {
                    "sizes_available": random.sample(["XS", "S", "M", "L", "XL", "XXL"], k=random.randint(2, 5)),
                    "colors": random.sample(["Black", "Navy Blue", "Heather Grey", "Olive Green", "Burgundy"], k=random.randint(1, 3)),
                    "material": random.choice(["100% Organic Cotton", "Polyester Blend", "Raw Denim", "Merino Wool"]),
                    "gender": random.choice(["Men", "Women", "Unisex"])
                },
                "tags": [sub.lower(), brand.lower(), "fashion", "apparel", "casual"]
            })
        elif cat == "Home Appliances":
            sub = random.choice(["Air Purifier", "Microwave Oven", "Robotic Vacuum", "Coffee Maker", "Blender"])
            price = round(random.uniform(3500, 48000), 2)
            base.update({
                "title": f"{brand} {sub} Series 7",
                "sub_category": sub,
                "price": price,
                "cost_price": round(price * 0.70, 2),
                "specifications": {
                    "power_watts": random.choice([600, 900, 1200, 1800, 2200]),
                    "energy_star_rating": random.randint(3, 5),
                    "voltage_v": 230,
                    "smart_wifi_enabled": random.choice([True, False]),
                    "warranty_years": random.choice([2, 5, 10])
                },
                "tags": [sub.lower(), brand.lower(), "home", "kitchen", "smart-appliance"]
            })
        elif cat == "Books":
            sub = random.choice(["Artificial Intelligence", "Data Engineering", "Cloud Computing", "Fiction", "History"])
            price = round(random.uniform(399, 2499), 2)
            base.update({
                "title": f"{brand} Guide to {sub} and Systems",
                "sub_category": sub,
                "price": price,
                "cost_price": round(price * 0.50, 2),
                "specifications": {
                    "isbn_13": f"978-{random.randint(1000000000, 9999999999)}",
                    "page_count": random.randint(220, 850),
                    "format": random.choice(["Hardcover", "Paperback", "Kindle Edition"]),
                    "language": "English",
                    "edition": f"{random.randint(1, 5)}th Edition"
                },
                "tags": ["book", sub.lower().replace(" ", "-"), "education", "reference"]
            })
        else: # Groceries
            sub = random.choice(["Breakfast Cereals", "Organic Dairy", "Green Teas", "Snack Nuts", "Cold Pressed Oils"])
            price = round(random.uniform(99, 1899), 2)
            base.update({
                "title": f"{brand} Premium {sub}",
                "sub_category": sub,
                "price": price,
                "cost_price": round(price * 0.65, 2),
                "specifications": {
                    "net_weight_grams": random.choice([250, 500, 1000, 2000]),
                    "is_organic_certified": random.choice([True, False]),
                    "shelf_life_months": random.choice([6, 12, 18, 24]),
                    "dietary_flags": random.sample(["Vegan", "Gluten-Free", "Non-GMO", "Sugar-Free"], k=random.randint(1, 2))
                },
                "tags": ["grocery", sub.lower().replace(" ", "-"), "organic", "food"]
            })

        products.append(base)

    return products

def run_mongodb_catalog_suite():
    print("=" * 70)
    print("STARTING ACTIVITY 4: MONGODB E-COMMERCE DYNAMIC CATALOG SYSTEM")
    print("=" * 70)

    client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
    db = client["ecommerce_catalog_db"]
    products_col = db["products"]

    # Clean collection for reproducible benchmark
    products_col.drop()
    print("✓ Initialized MongoDB database 'ecommerce_catalog_db' and collection 'products'.")

    # -----------------------------------------------------------------
    # STEP 1: BULK DOCUMENT INSERTION (POLYMORPHIC SCHEMAS)
    # -----------------------------------------------------------------
    print("\n[CRUD 1: Create / Bulk Insert] Generating & inserting 15,000 heterogeneous catalog documents...")
    docs = generate_catalog_documents(num_products=15000)
    t0 = time.time()
    result = products_col.insert_many(docs)
    insert_duration = round(time.time() - t0, 3)
    print(f"✓ Inserted {len(result.inserted_ids):,} products into MongoDB in {insert_duration}s.")

    # Save sample product documents to JSON for report verification
    sample_docs = list(products_col.find({}, {"_id": 0}).limit(3))
    with open("activity4_mongodb/sample_catalog_documents.json", "w", encoding="utf-8") as f:
        json.dump(sample_docs, f, indent=2, default=str)
    print("✓ Saved sample heterogeneous BSON documents to activity4_mongodb/sample_catalog_documents.json")

    # -----------------------------------------------------------------
    # STEP 2: ADVANCED FILTERING & PROJECTION (READ)
    # -----------------------------------------------------------------
    print("\n[CRUD 2: Read / Advanced Query] Finding high-end Electronics within price range ₹30,000 - ₹90,000...")
    search_filter = {
        "category": "Electronics",
        "price": {"$gte": 30000, "$lte": 90000},
        "stock_quantity": {"$gt": 10}
    }
    sample_search = list(products_col.find(search_filter, {"_id": 0, "title": 1, "brand": 1, "price": 1, "stock_quantity": 1, "specifications.ram_gb": 1}).limit(5))
    print(f"Found {products_col.count_documents(search_filter):,} matching products. Sample Results:")
    for item in sample_search:
        print(f"  • [{item['brand']}] {item['title']} - ₹{item['price']:,.2f} (Stock: {item['stock_quantity']})")

    # -----------------------------------------------------------------
    # STEP 3: ATOMIC UPDATES ($inc, $set, $push)
    # -----------------------------------------------------------------
    print("\n[CRUD 3: Update / Atomic Operations] Executing order purchase simulation & stock decrement...")
    target_sku = sample_search[0]["title"]
    sample_item = products_col.find_one({"title": target_sku})
    old_stock = sample_item["stock_quantity"]

    update_res = products_col.update_one(
        {"sku": sample_item["sku"]},
        {
            "$inc": {"stock_quantity": -3},
            "$set": {"last_sold_at": datetime.now()},
            "$push": {
                "audit_log": {
                    "action": "ORDER_FULFILLED",
                    "units": 3,
                    "timestamp": datetime.now()
                }
            }
        }
    )
    new_stock = products_col.find_one({"sku": sample_item["sku"]})["stock_quantity"]
    print(f"✓ Atomically updated SKU '{sample_item['sku']}': Stock changed from {old_stock} to {new_stock} (Modified: {update_res.modified_count}).")

    # -----------------------------------------------------------------
    # STEP 4: SOFT & HARD DELETION (DELETE)
    # -----------------------------------------------------------------
    print("\n[CRUD 4: Delete / Life Cycle Management] Decommissioning discontinued products...")
    # Soft delete: Mark obsolete products with low rating and zero stock as discontinued
    soft_del = products_col.update_many(
        {"stock_quantity": 0, "rating.average": {"$lt": 3.4}},
        {"$set": {"is_discontinued": True, "is_active": False}}
    )
    print(f"✓ Soft-deleted {soft_del.modified_count} obsolete products (flagged is_discontinued=True).")

    # Hard delete: Remove discontinued items marked for archival
    hard_del = products_col.delete_many({"is_discontinued": True, "stock_quantity": 0})
    print(f"✓ Hard-deleted {hard_del.deleted_count} discontinued products from active catalog.")

    # -----------------------------------------------------------------
    # STEP 5: AGGREGATION PIPELINE (ANALYTICS & METRICS)
    # -----------------------------------------------------------------
    print("\n[Aggregation Pipeline] Computing category-wise inventory value, average pricing, and ratings...")
    pipeline = [
        {"$match": {"is_active": True}},
        {
            "$group": {
                "_id": "$category",
                "total_products": {"$sum": 1},
                "total_inventory_units": {"$sum": "$stock_quantity"},
                "avg_price": {"$avg": "$price"},
                "min_price": {"$min": "$price"},
                "max_price": {"$max": "$price"},
                "avg_rating": {"$avg": "$rating.average"},
                "total_inventory_valuation": {"$sum": {"$multiply": ["$price", "$stock_quantity"]}}
            }
        },
        {"$sort": {"total_inventory_valuation": -1}}
    ]

    agg_results = list(products_col.aggregate(pipeline))
    df_agg = pd.DataFrame(agg_results).rename(columns={"_id": "category"})
    df_agg["avg_price"] = df_agg["avg_price"].round(2)
    df_agg["avg_rating"] = df_agg["avg_rating"].round(2)
    df_agg["total_inventory_valuation"] = df_agg["total_inventory_valuation"].round(2)
    df_agg.to_csv("activity4_mongodb/category_aggregation_summary.csv", index=False)
    print("\n[Category Aggregation Results]")
    print(df_agg[["category", "total_products", "total_inventory_units", "avg_price", "total_inventory_valuation"]].to_string(index=False))

    # -----------------------------------------------------------------
    # STEP 6: INDEXING BENCHMARK & EXPLAIN PLAN (COLLSCAN vs IXSCAN)
    # -----------------------------------------------------------------
    print("\n[Indexing Benchmark & Explain Plan Analysis]")
    query_bench = {
        "category": "Electronics",
        "price": {"$gte": 25000, "$lte": 75000}
    }

    # 1. Unindexed Performance (COLLSCAN)
    products_col.drop_indexes() # Ensure clean state (only _id_)
    explain_unindexed = products_col.find(query_bench).explain()["executionStats"]
    
    # Measure latency over 50 iterations
    t_start = time.time()
    for _ in range(50):
        list(products_col.find(query_bench).limit(50))
    time_unindexed_ms = round(((time.time() - t_start) / 50.0) * 1000.0, 3)

    print("\n--- Phase A: Without Index (COLLSCAN) ---")
    print(f"  • Execution Stage: {explain_unindexed['executionStages'].get('stage')}")
    print(f"  • Total Documents Examined: {explain_unindexed['totalDocsExamined']:,}")
    print(f"  • Documents Returned: {explain_unindexed['nReturned']:,}")
    print(f"  • Average Latency: {time_unindexed_ms} ms")

    # 2. Create Compound Index
    print("\nCreating Compound B-Tree Index: {'category': 1, 'price': 1}...")
    products_col.create_index([("category", pymongo.ASCENDING), ("price", pymongo.ASCENDING)])
    products_col.create_index([("sku", pymongo.ASCENDING)], unique=True)
    products_col.create_index([("tags", pymongo.ASCENDING)]) # Multikey index
    print("✓ Indexes created successfully.")

    # 3. Indexed Performance (IXSCAN)
    explain_indexed = products_col.find(query_bench).explain()["executionStats"]
    
    t_start = time.time()
    for _ in range(50):
        list(products_col.find(query_bench).limit(50))
    time_indexed_ms = round(((time.time() - t_start) / 50.0) * 1000.0, 3)

    stage_indexed = explain_indexed['executionStages'].get('stage')
    if 'inputStage' in explain_indexed['executionStages']:
        stage_indexed = f"{stage_indexed} -> {explain_indexed['executionStages']['inputStage'].get('stage')}"

    print("\n--- Phase B: With Compound Index (IXSCAN) ---")
    print(f"  • Execution Stage: {stage_indexed}")
    print(f"  • Total Documents Examined: {explain_indexed['totalDocsExamined']:,}")
    print(f"  • Documents Returned: {explain_indexed['nReturned']:,}")
    print(f"  • Average Latency: {time_indexed_ms} ms")
    
    speedup = round(time_unindexed_ms / max(0.001, time_indexed_ms), 1)
    doc_reduction_pct = round(((explain_unindexed['totalDocsExamined'] - explain_indexed['totalDocsExamined']) / explain_unindexed['totalDocsExamined']) * 100, 1)
    print(f"\n✓ Optimization Summary: {speedup}x Speedup | {doc_reduction_pct}% Fewer Documents Scanned!")

    # Save benchmark metrics to CSV
    benchmark_df = pd.DataFrame([
        {
            "Metric": "Query Execution Stage",
            "Without_Index": "COLLSCAN (Collection Scan)",
            "With_Compound_Index": "IXSCAN (B-Tree Index Scan)"
        },
        {
            "Metric": "Total Docs Examined",
            "Without_Index": explain_unindexed['totalDocsExamined'],
            "With_Compound_Index": explain_indexed['totalDocsExamined']
        },
        {
            "Metric": "Query Latency (ms)",
            "Without_Index": time_unindexed_ms,
            "With_Compound_Index": time_indexed_ms
        },
        {
            "Metric": "Documents Returned",
            "Without_Index": explain_unindexed['nReturned'],
            "With_Compound_Index": explain_indexed['nReturned']
        }
    ])
    benchmark_df.to_csv("activity4_mongodb/benchmark_results.csv", index=False)

    # -----------------------------------------------------------------
    # STEP 7: VISUALIZATIONS GENERATION
    # -----------------------------------------------------------------
    print("\nGenerating MongoDB performance and catalog visualizations...")

    # Chart 1: Indexing Benchmark Comparison (COLLSCAN vs IXSCAN)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.2))

    # Docs Examined
    stages = ['Unindexed\n(COLLSCAN)', 'Compound Index\n(IXSCAN)']
    docs_scanned = [explain_unindexed['totalDocsExamined'], explain_indexed['totalDocsExamined']]
    bars1 = ax1.bar(stages, docs_scanned, color=['#e74c3c', '#2ecc71'], width=0.5, edgecolor='black')
    ax1.set_ylabel('Documents Examined in Memory', fontweight='bold')
    ax1.set_title('Disk/Memory Scan Efficiency', fontweight='bold', fontsize=12)
    for b in bars1:
        h = b.get_height()
        ax1.text(b.get_x() + b.get_width()/2, h + 200, f'{h:,}', ha='center', fontweight='bold')
    ax1.grid(axis='y', linestyle='--', alpha=0.7)

    # Query Latency
    latencies = [time_unindexed_ms, time_indexed_ms]
    bars2 = ax2.bar(stages, latencies, color=['#e74c3c', '#2ecc71'], width=0.5, edgecolor='black')
    ax2.set_ylabel('Average Query Latency (Milliseconds)', fontweight='bold')
    ax2.set_title(f'Query Execution Speed ({speedup}x Improvement)', fontweight='bold', fontsize=12)
    for b in bars2:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2, h + 0.1, f'{h:.2f} ms', ha='center', fontweight='bold')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    plt.suptitle('MongoDB Performance Benchmark: Impact of Compound Index {category: 1, price: 1}', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig("visualizations/activity4_mongodb_index_benchmark.png", dpi=300, bbox_inches='tight')
    plt.close()

    # Chart 2: Category Inventory Valuation and Average Price
    fig, ax1 = plt.subplots(figsize=(11, 5.5))
    ax2 = ax1.twinx()

    x = np.arange(len(df_agg))
    w = 0.35
    ax1.bar(x - w/2, df_agg["total_inventory_valuation"] / 1e7, width=w, color="#3498db", label="Inventory Valuation (Crores ₹)")
    ax2.bar(x + w/2, df_agg["avg_price"], width=w, color="#f39c12", label="Average Product Price (₹)")

    ax1.set_ylabel("Inventory Valuation (Crores INR ₹)", color="#2980b9", fontweight="bold")
    ax2.set_ylabel("Average Item Price (₹)", color="#d35400", fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_agg["category"], fontweight="bold")
    ax1.set_title("MongoDB Aggregation Pipeline: Inventory Capitalization & Pricing by Category", fontsize=13, fontweight="bold", pad=15)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
    ax1.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig("visualizations/activity4_mongodb_category_stats.png", dpi=300)
    plt.close()

    # Chart 3: Schema Comparison Diagram: RDBMS Normalization vs MongoDB Document Model
    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.axis("off")

    # Title
    ax.text(0.5, 0.95, "Architectural Comparison: Relational (RDBMS) vs. MongoDB Document Model", 
            ha="center", va="center", fontsize=14, fontweight="bold", color="#2c3e50")

    # RDBMS Box (Left)
    rdbms_box = plt.Rectangle((0.03, 0.08), 0.44, 0.78, fill=True, color="#ebf5fb", ec="#2980b9", lw=2, transform=ax.transAxes)
    ax.add_patch(rdbms_box)
    ax.text(0.25, 0.81, "Relational Database Model (3NF Normalization)", ha="center", va="center", fontsize=12, fontweight="bold", color="#1b4f72", transform=ax.transAxes)

    rdbms_text = (
        "• Rigid Pre-defined Table Schemas\n"
        "• Products Table (id, name, brand, price)\n"
        "• Product_Specs Table (id, prod_id, spec_name, val)\n"
        "• Product_Tags Junction Table (prod_id, tag_id)\n"
        "• Product_Reviews Table (id, prod_id, rating, user)\n"
        "• Requires Multi-Way JOINs (Costly O(N log N))\n"
        "• ALTER TABLE requires global schema lock\n"
        "• Vertical scaling bottleneck; complex sharding"
    )
    ax.text(0.06, 0.45, rdbms_text, ha="left", va="center", fontsize=10.5, linespacing=1.6, color="#2c3e50", transform=ax.transAxes)

    # MongoDB Box (Right)
    mongo_box = plt.Rectangle((0.53, 0.08), 0.44, 0.78, fill=True, color="#eafaf1", ec="#27ae60", lw=2, transform=ax.transAxes)
    ax.add_patch(mongo_box)
    ax.text(0.75, 0.81, "MongoDB Document Model (Self-Contained BSON)", ha="center", va="center", fontsize=12, fontweight="bold", color="#145a32", transform=ax.transAxes)

    mongo_text = (
        "• Dynamic Polymorphic Schema (Heterogeneous)\n"
        "• Single Self-Contained Document per Product\n"
        "• Nested Sub-documents for Category Specs\n"
        "• Embedded Arrays for Tags, Sizes, Reviews\n"
        "• Zero Multi-Table JOIN Latency (Single IO seek)\n"
        "• Zero-Downtime Schema Evolution\n"
        "• Native Compound & Multikey B-Tree Indexing\n"
        "• Horizontal Auto-Sharding across cluster nodes"
    )
    ax.text(0.56, 0.45, mongo_text, ha="left", va="center", fontsize=10.5, linespacing=1.6, color="#2c3e50", transform=ax.transAxes)

    plt.tight_layout()
    plt.savefig("visualizations/activity4_mongodb_schema_diagram.png", dpi=300)
    plt.close()

    print("✓ All 3 MongoDB visualizations generated and saved in visualizations/")
    print("=" * 70)
    print("ACTIVITY 4 COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    run_mongodb_catalog_suite()

