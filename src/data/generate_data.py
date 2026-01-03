import polars as pl
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()
random.seed(42)

# Configuration
NUM_CUSTOMERS = 5000
NUM_PRODUCTS = 500
NUM_TRANSACTIONS = 100000

print("🚀 Generating RetailPulse synthetic dataset...")

# Generate customers
print("👥 Creating customers...")
customers = []
for i in range(NUM_CUSTOMERS):
    customers.append({
        'customer_id': f'C{i + 1:05d}',
        'name': fake.name(),
        'email': fake.email(),
        'city': fake.city(),
        'state': fake.state(),
        'country': 'India',
        'join_date': fake.date_between(start_date='-3y', end_date='today')
    })

df_customers = pl.DataFrame(customers)
df_customers.write_csv('data/raw/customers.csv')
print(f"✅ Created {len(customers)} customers")

# Generate products
print("📦 Creating products...")
categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports', 'Beauty', 'Toys']
products = []
for i in range(NUM_PRODUCTS):
    products.append({
        'product_id': f'P{i + 1:05d}',
        'product_name': fake.catch_phrase(),
        'category': random.choice(categories),
        'price': round(random.uniform(10, 500), 2),
        'cost': round(random.uniform(5, 300), 2)
    })

df_products = pl.DataFrame(products)
df_products.write_csv('data/raw/products.csv')
print(f"✅ Created {len(products)} products")

# Generate transactions
print("💳 Creating transactions...")
transactions = []
for i in range(NUM_TRANSACTIONS):
    customer = random.choice(customers)
    product = random.choice(products)
    quantity = random.randint(1, 5)

    transactions.append({
        'transaction_id': f'T{i + 1:08d}',
        'customer_id': customer['customer_id'],
        'product_id': product['product_id'],
        'quantity': quantity,
        'price': product['price'],
        'total_amount': round(product['price'] * quantity, 2),
        'transaction_date': fake.date_between(start_date='-1y', end_date='today'),
        'payment_method': random.choice(['Credit Card', 'Debit Card', 'UPI', 'Cash'])
    })

df_transactions = pl.DataFrame(transactions)
df_transactions.write_csv('data/raw/transactions.csv')
print(f"✅ Created {len(transactions)} transactions")

print("\n🎉 Dataset generation complete!")
print(f"📁 Files saved in data/raw/")