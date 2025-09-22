from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models
from app.database import SessionLocal, engine
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import Form
from starlette.responses import RedirectResponse
import pandas as pd
from sqlalchemy import func

def populate_db_from_excel(file_path='fake_coffee_data.xlsx'):
    customers_df = pd.read_excel(file_path, sheet_name='customers')
    products_df = pd.read_excel(file_path, sheet_name='products')
    orders_df = pd.read_excel(file_path, sheet_name='orders')
    inventory_df = pd.read_excel(file_path, sheet_name='inventory')

    db: Session = SessionLocal()

    # Clear existing data
    db.query(models.Order).delete()
    db.query(models.Product).delete()
    db.query(models.Customer).delete()
    db.query(models.Inventory).delete()
    db.commit()

    # Populate customers

    for _, row in customers_df.iterrows():
        db_customer = models.Customer(name=row['name'], email=row['email'])
        db.add(db_customer)

    # Populate products
    for _, row in products_df.iterrows():
        db_product = models.Product(
            name=row['name'],
            description=row['description'],
            price=row['price']
        )
        db.add(db_product)

    # Map product and customer IDs correctly
    customer_map = {c.email: c.id for c in db.query(models.Customer).all()}
    product_map = {p.name: p.id for p in db.query(models.Product).all()}

    # Populate orders
    for _, row in orders_df.iterrows():
        db_order = models.Order(
            customer_id=int(row['customer_id']),
            product_id=int(row['product_id']),
            quantity=int(row['quantity'])
        )
        db.add(db_order)
    # Populate inventory

    for _, row in inventory_df.iterrows():
        db_inventory = models.Inventory(
            product_id=int(row['product_id']),
            stock_level=int(row['stock_level'])
        )
        db.add(db_inventory)
    db.commit()


# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

populate_db_from_excel('fake_coffee_data.xlsx')  # Populate the database from the Excel file on startup

# Connect to the database temporarily to verify connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Refresh the data

@app.get("/refresh")
def refresh_excel_data():
    populate_db_from_excel("fake_coffee_data.xlsx")
    return RedirectResponse(url="/", status_code=303)
# Customers endpoint

class CustomerCreate(BaseModel):
    name: str
    email: str

@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    #Top Customers by number of orders
    top_customers = (db.query(
        models.Customer.name,
        func.sum(models.Order.quantity * models.Product.price).label('total_spent')
    )
    .join(models.Order)
    .join(models.Product)
    .group_by(models.Customer.id)
    .order_by(func.sum(models.Order.quantity * models.Product.price).desc())
    .limit(5)
    .all()
)
    #Best Selling Products
    top_products = (db.query(
        models.Product.name,
        func.sum(models.Order.quantity).label('total_sold')
    )
    .join(models.Order)
    .group_by(models.Product.id)
    .order_by(func.sum(models.Order.quantity).desc())
    .limit(5)
    .all()
    )

    stock_summary = (
        db.query(
            models.Product.name,
            models.Inventory.stock_level
        )
        .join(models.Inventory, models.Product.id == models.Inventory.product_id)
        .all()
    )

    return templates.TemplateResponse("index.html", {
        "request": request,
        "top_customers": top_customers,
        "top_products": top_products,
        "stock_summary": stock_summary
    })

@app.get("/customers")
def customers_page(request: Request, db: Session = Depends(get_db)):
    customers = db.query(models.Customer).all()
    return templates.TemplateResponse("customers.html", {"request": request, "customers": customers})

@app.post("/customers")
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = models.Customer(name = customer.name, email = customer.email)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# Create a new customer
@app.post("/customers/")
def create_customer(
    name: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    new_customer = models.Customer(name=name, email=email)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return RedirectResponse(url="/customers", status_code=303)

# Products endpoint

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float

@app.get("/products")
def products_page(request: Request, db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return templates.TemplateResponse("products.html", {"request": request, "products": products})

@app.post("/products")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(name = product.name, description = product.description, price = product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Create a new product
@app.post("/products/")
def create_product(
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    db: Session = Depends(get_db)
):
    new_product = models.Product(name=name, description=description, price=price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return RedirectResponse(url="/products", status_code=303)
# Orders endpoint

class OrderCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int

@app.get("/orders")
def orders_page(request: Request, db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    customers = db.query(models.Customer).all()
    products = db.query(models.Product).all()
    return templates.TemplateResponse("orders.html", {
        "request": request,
        "orders": orders,
        "customers": customers,
        "products": products
    })

@app.post("/orders")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(customer_id = order.customer_id, product_id = order.product_id, quantity = order.quantity)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# Create a new order
@app.post("/orders/")
def create_order(
    customer_id: int = Form(...),
    product_id: int = Form(...),
    quantity: int = Form(...),
    db: Session = Depends(get_db)
):
    new_order = models.Order(customer_id=customer_id, product_id=product_id, quantity=quantity)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return RedirectResponse(url="/orders", status_code=303)

# Inventory endpoint
@app.get("/inventory")
def inventory_page(request: Request, db: Session = Depends(get_db)):
    inventory = db.query(models.Inventory).all()
    products = db.query(models.Product).all()
    return templates.TemplateResponse("inventory.html", {
        "request": request,
        "inventory": inventory,
        "products": products
    })

@app.post("/inventory/")
def create_or_update_inventory(
    product_id: int = Form(...),
    stock_level: int = Form(...),
    db: Session = Depends(get_db)
):
    inventory_item = db.query(models.Inventory).filter(models.Inventory.product_id == product_id).first()
    if inventory_item:
        inventory_item.stock_level = stock_level
    else:
        inventory_item = models.Inventory(product_id=product_id, stock_level=stock_level)
        db.add(inventory_item)
    db.commit()
    db.refresh(inventory_item)
    return RedirectResponse(url="/inventory", status_code=303)