# populate_db.py
from sqlalchemy.orm import Session
from app import models
from app.database import SessionLocal, engine

# --- Sample data ---

customers = [
    {"name": "Alice Johnson", "email": "alice.johnson@example.com"},
    {"name": "Bob Smith", "email": "bob.smith@example.com"},
    {"name": "Charlie Brown", "email": "charlie.brown@example.com"},
    {"name": "Diana Prince", "email": "diana.prince@example.com"},
    {"name": "Ethan Hunt", "email": "ethan.hunt@example.com"},
    {"name": "Fiona Gallagher", "email": "fiona.gallagher@example.com"},
    {"name": "George Martin", "email": "george.martin@example.com"},
    {"name": "Hannah Baker", "email": "hannah.baker@example.com"},
    {"name": "Ian Wright", "email": "ian.wright@example.com"},
    {"name": "Julia Roberts", "email": "julia.roberts@example.com"}
]

products = [
    {"name": "Ethiopian Yirgacheffe", "description": "Floral, light roast, medium acidity", "price": 15.00},
    {"name": "Colombian Supremo", "description": "Rich, nutty, medium-dark roast", "price": 13.00},
    {"name": "Guatemalan Antigua", "description": "Chocolatey, full body, balanced acidity", "price": 14.00},
    {"name": "Kenyan AA", "description": "Bright, fruity, light roast", "price": 16.50},
    {"name": "Brazil Santos", "description": "Nutty, chocolate notes, medium roast", "price": 12.00},
    {"name": "Sumatra Mandheling", "description": "Earthy, full body, low acidity", "price": 17.00},
    {"name": "Costa Rican Tarrazu", "description": "Clean, bright, medium roast", "price": 14.50},
    {"name": "Panama Geisha", "description": "Floral, delicate, highly sought after", "price": 25.00},
    {"name": "Honduras Marcala", "description": "Sweet, nutty, medium roast", "price": 13.50},
    {"name": "Rwanda Bourbon", "description": "Fruity, light body, aromatic", "price": 15.50}
]

orders = [
    {"customer_id": 1, "product_id": 1, "quantity": 2},
    {"customer_id": 2, "product_id": 2, "quantity": 1},
    {"customer_id": 3, "product_id": 3, "quantity": 3},
    {"customer_id": 4, "product_id": 4, "quantity": 1},
    {"customer_id": 5, "product_id": 5, "quantity": 2},
    {"customer_id": 6, "product_id": 6, "quantity": 1},
    {"customer_id": 7, "product_id": 7, "quantity": 2},
    {"customer_id": 8, "product_id": 8, "quantity": 1},
    {"customer_id": 9, "product_id": 9, "quantity": 3},
    {"customer_id": 10, "product_id": 10, "quantity": 2}
]

# --- Populate database ---
def populate():
    db: Session = SessionLocal()
    
    # Add customers
    for c in customers:
        db_customer = models.Customer(name=c["name"], email=c["email"])
        db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    # Add products
    for p in products:
        db_product = models.Product(name=p["name"], description=p["description"], price=p["price"])
        db.add(db_product)
    db.commit()
    db.refresh(db_product)
    # Add orders
    for o in orders:
        db_order = models.Order(customer_id=o["customer_id"], product_id=o["product_id"], quantity=o["quantity"])
        db.add(db_order)
    db.commit()
    db.refresh(db_order)
    db.close()
    print("Database populated successfully!")

if __name__ == "__main__":
    populate()
