import pandas as pd
import numpy as np

np.random.seed(42)

n = 1000

customer_ids = [
    f"CUST{str(i).zfill(4)}"
    for i in range(1, n + 1)
]

countries = np.random.choice(
    ["India", "USA", "UK", "Germany", "France", "Canada"],
    n,
    p=[0.35, 0.20, 0.15, 0.10, 0.10, 0.10]
)

genders = np.random.choice(
    ["Male", "Female"],
    n
)

ages = np.random.randint(18, 65, n)

purchase_frequency = np.random.randint(1, 21, n)

average_order_value = np.round(
    np.random.uniform(500, 5000, n),
    2
)

total_purchases = np.round(
    purchase_frequency * average_order_value,
    2
)

recency_days = np.random.randint(1, 181, n)

total_items = np.random.randint(1, 101, n)

categories = np.random.choice(
    [
        "Electronics",
        "Clothing",
        "Home & Kitchen",
        "Beauty",
        "Sports"
    ],
    n
)

customers = pd.DataFrame({
    "customer_id": customer_ids,
    "country": countries,
    "gender": genders,
    "age": ages,
    "purchase_frequency": purchase_frequency,
    "average_order_value": average_order_value,
    "total_purchases": total_purchases,
    "recency_days": recency_days,
    "total_items": total_items,
    "favorite_category": categories
})

customers.to_csv(
    "data/retail_customers.csv",
    index=False
)

print("Dataset created successfully!")
print(f"Rows: {len(customers)}")
print(customers.head())