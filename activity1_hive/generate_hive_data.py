"""
Supermarket Sales Transaction Dataset Generator for Apache Hive Analysis.
Simulates a realistic multi-branch supermarket chain over a 12-month period.
"""

import csv
import random
from datetime import datetime, timedelta

def generate_supermarket_data(filename="activity1_hive/supermarket_sales.csv", num_records=25000):
    random.seed(42)
    
    branches = [
        {"branch_id": "BR-101", "branch_name": "Metro Central", "city": "Bengaluru", "region": "South"},
        {"branch_id": "BR-102", "branch_name": "Indiranagar Galleria", "city": "Bengaluru", "region": "South"},
        {"branch_id": "BR-103", "branch_name": "Whitefield Hub", "city": "Bengaluru", "region": "South"},
        {"branch_id": "BR-104", "branch_name": "Bandra Arcade", "city": "Mumbai", "region": "West"},
        {"branch_id": "BR-105", "branch_name": "Andheri MegaStore", "city": "Mumbai", "region": "West"},
        {"branch_id": "BR-106", "branch_name": "Connaught Place Super", "city": "Delhi", "region": "North"},
        {"branch_id": "BR-107", "branch_name": "Gurugram CyberHub", "city": "Delhi NCR", "region": "North"},
        {"branch_id": "BR-108", "branch_name": "Hitech City Mart", "city": "Hyderabad", "region": "South"}
    ]
    
    categories = {
        "Dairy & Breakfast": [
            ("Organic Milk 1L", 65.0, 52.0),
            ("Greek Yogurt 400g", 120.0, 95.0),
            ("Salted Butter 500g", 275.0, 230.0),
            ("Multigrain Bread 400g", 55.0, 42.0),
            ("Eggs Pack of 12", 90.0, 72.0)
        ],
        "Fresh Produce": [
            ("Farm Fresh Tomatoes 1kg", 45.0, 30.0),
            ("Red Onions 1kg", 38.0, 25.0),
            ("Shimla Apples 1kg", 180.0, 135.0),
            ("Cavendish Bananas 1kg", 50.0, 35.0),
            ("Baby Spinach 250g", 40.0, 26.0)
        ],
        "Packaged Foods & Snacks": [
            ("Whole Wheat Pasta 500g", 110.0, 85.0),
            ("Extra Virgin Olive Oil 1L", 850.0, 680.0),
            ("Dark Chocolate 100g", 160.0, 115.0),
            ("Roasted Almonds 250g", 340.0, 270.0),
            ("Digestive Biscuits 300g", 75.0, 58.0)
        ],
        "Beverages": [
            ("Arabica Coffee Beans 250g", 420.0, 310.0),
            ("Green Tea Bags 50s", 210.0, 160.0),
            ("Cold Pressed Orange Juice 1L", 150.0, 110.0),
            ("Sparkling Mineral Water 750ml", 85.0, 55.0),
            ("Oat Milk 1L", 240.0, 185.0)
        ],
        "Household & Hygiene": [
            ("Eco Dishwash Gel 750ml", 145.0, 105.0),
            ("Floor Cleaner Lemon 1L", 195.0, 140.0),
            ("Laundry Detergent Liquid 2L", 499.0, 380.0),
            ("Bamboo Paper Towels 2pk", 165.0, 120.0),
            ("Biodegradable Trash Bags 30s", 130.0, 90.0)
        ],
        "Personal Care": [
            ("Herbal Shampoo 340ml", 320.0, 240.0),
            ("Aloe Vera Body Wash 400ml", 280.0, 205.0),
            ("Fluoride Free Toothpaste 150g", 115.0, 82.0),
            ("Organic Sunscreen SPF50 100ml", 450.0, 320.0),
            ("Hydrating Face Moisturizer 50g", 390.0, 275.0)
        ]
    }
    
    payment_methods = ["Credit Card", "UPI", "Debit Card", "Digital Wallet", "Cash"]
    payment_weights = [0.35, 0.40, 0.12, 0.08, 0.05]
    
    customer_types = ["Member (Gold)", "Member (Silver)", "Regular", "First-time"]
    customer_weights = [0.25, 0.35, 0.30, 0.10]
    
    start_date = datetime(2025, 1, 1, 8, 0, 0)
    
    fieldnames = [
        "transaction_id", "timestamp", "date", "year_month", "hour_of_day",
        "branch_id", "branch_name", "city", "region", "customer_type",
        "product_name", "category", "unit_price", "unit_cost", "quantity",
        "gross_revenue", "total_cost", "net_profit", "payment_method", "discount_applied"
    ]
    
    print(f"Generating {num_records} synthetic supermarket transactions...")
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(1, num_records + 1):
            # Days offset over 365 days
            day_offset = random.randint(0, 364)
            
            # Hourly distribution: Peak between 10-13 and 17-21
            hour_weights = [
                0, 0, 0, 0, 0, 0, 0, 1,    # 0-7 (Closed/Opening)
                3, 6, 9, 8, 7, 5,          # 8-13 (Morning rush)
                4, 5, 7, 10, 12, 11, 8,    # 14-20 (Evening peak)
                4, 2, 0                    # 21-23 (Closing)
            ]
            hour = random.choices(range(24), weights=hour_weights)[0]
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            
            tx_time = start_date + timedelta(days=day_offset, hours=hour, minutes=minute, seconds=second)
            
            branch = random.choice(branches)
            cat_name = random.choice(list(categories.keys()))
            prod_info = random.choice(categories[cat_name])
            prod_name, unit_price, unit_cost = prod_info
            
            # Quantities: mostly 1-4, rarely 5-8
            quantity = random.choices([1, 2, 3, 4, 5, 6, 8], weights=[40, 30, 15, 8, 4, 2, 1])[0]
            
            # Member discounts
            cust_type = random.choices(customer_types, weights=customer_weights)[0]
            discount_pct = 0.0
            if cust_type == "Member (Gold)":
                discount_pct = 0.10
            elif cust_type == "Member (Silver)":
                discount_pct = 0.05
            
            gross_revenue = round(unit_price * quantity * (1.0 - discount_pct), 2)
            total_cost = round(unit_cost * quantity, 2)
            net_profit = round(gross_revenue - total_cost, 2)
            
            payment = random.choices(payment_methods, weights=payment_weights)[0]
            
            row = {
                "transaction_id": f"TXN-{2025000000 + i}",
                "timestamp": tx_time.strftime("%Y-%m-%d %H:%M:%S"),
                "date": tx_time.strftime("%Y-%m-%d"),
                "year_month": tx_time.strftime("%Y-%m"),
                "hour_of_day": hour,
                "branch_id": branch["branch_id"],
                "branch_name": branch["branch_name"],
                "city": branch["city"],
                "region": branch["region"],
                "customer_type": cust_type,
                "product_name": prod_name,
                "category": cat_name,
                "unit_price": unit_price,
                "unit_cost": unit_cost,
                "quantity": quantity,
                "gross_revenue": gross_revenue,
                "total_cost": total_cost,
                "net_profit": net_profit,
                "payment_method": payment,
                "discount_applied": discount_pct
            }
            writer.writerow(row)
            
    print(f"Dataset generated successfully: {filename} ({num_records} records)")

if __name__ == "__main__":
    generate_supermarket_data()

