from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models
from app.database import SessionLocal, engine
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi import Request

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Connect to the database temporarily to verify connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Customers endpoint

class CustomerCreate(BaseModel):
    name: str
    email: str

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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

# Orders endpoint

class OrderCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int

@app.get("/orders")
def orders_page(request: Request, db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})

@app.post("/orders")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(customer_id = order.customer_id, product_id = order.product_id, quantity = order.quantity)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order