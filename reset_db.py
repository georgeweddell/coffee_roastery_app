# reset_db.py
from app import models
from app.database import engine

def reset_database():
    # Drop all tables
    models.Base.metadata.drop_all(bind=engine)
    print("All tables dropped.")
    
    # Recreate all tables
    models.Base.metadata.create_all(bind=engine)
    print("All tables created.")

if __name__ == "__main__":
    reset_database()