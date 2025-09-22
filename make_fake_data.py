from faker import Faker
import pandas as pd

fake = Faker()

customers = []

for i in range(100):
    customers.append({
        "id": i+1,  # give them a simple numeric ID
        "name": fake.name(),
        "email": fake.unique.email()
    })

customers_df = pd.DataFrame(customers)
print(customers_df)

products = []
product_names = [
    "Ethiopian Yirgacheffe", "Colombian Supremo", "Guatemalan Antigua",
    "Kenyan AA", "Brazil Santos", "Sumatra Mandheling", "Costa Rican Tarrazu",
    "Panama Geisha", "Honduras Marcala", "Rwanda Bourbon"]
descriptions = [
    "Floral, light roast, medium acidity", "Rich, nutty, medium-dark roast",
    "Chocolatey, full body, balanced acidity", "Bright, fruity, light roast",
    "Nutty, chocolate notes, medium roast", "Earthy, full body, low acidity",
    "Clean, bright, medium roast", "Floral, delicate, highly sought after",
    "Sweet, nutty, medium roast", "Fruity, light body, aromatic"
]
prices = [15.00, 13.00, 14.00, 16.50, 12.00, 17.00, 14.50, 25.00, 13.50, 15.50]

for i in range(len(product_names)):
    products.append({
        "id": i+1,
        "name": product_names[i],
        "description": descriptions[i],
        "price": prices[i]
    })

products_df = pd.DataFrame(products)
print(products_df)

orders = []
import random

for i in range(100):
    orders.append({
        "id": i+1,
        "customer_id": random.randint(1, 100),
        "product_id": random.randint(1, 10),
        "quantity": random.randint(1, 5)
    })

orders_df = pd.DataFrame(orders)
print(orders_df)

Inventory = []
for product in products:
    Inventory.append({
        "product_id": product["id"],
        "stock_level": random.randint(20, 100)
    })
inventory_df = pd.DataFrame(Inventory)
print(inventory_df)

with pd.ExcelWriter('fake_coffee_data.xlsx', engine='openpyxl') as writer:
    customers_df.to_excel(writer, sheet_name='customers', index=False)
    products_df.to_excel(writer, sheet_name='products', index=False)
    orders_df.to_excel(writer, sheet_name='orders', index=False)
    inventory_df.to_excel(writer, sheet_name='inventory', index=False)
    

print("Fake data written to fake_coffee_data.xlsx")