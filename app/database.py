from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database configuration
DATABASE_URL = "sqlite:///coffee_roastery.db"

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args = {"check_same_thread": False})

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# Create a base class for declarative class definitions
Base = declarative_base()