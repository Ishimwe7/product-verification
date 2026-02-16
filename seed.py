import os
import uuid
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.repositories import ProductModel, Base

# 1. Load Environment Variables
load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER", "Nyanja")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "Nyanja")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DB", "product_db")

# 2. Build Connection URL
MYSQL_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# 3. Database Setup
engine = create_engine(MYSQL_URL)
SessionLocal = sessionmaker(bind=engine)

def seed_data():
    db = SessionLocal()
    
    # Optional: Clear existing data to avoid duplicates during testing
    # db.query(ProductModel).delete()
    
    products = [
        ProductModel(
            id=str(uuid.uuid4()),
            name="Professional Camera",
            category="Electronics",
            price=1200.00,
            currency="USD",
            stock_quantity=10,
            assets=json.dumps(["https://example.com/cam1.jpg"]), 
            status="pending_verification"
        ),
        ProductModel(
            id=str(uuid.uuid4()),
            name="Invalid Product (Negative Price)",
            category="Testing",
            price=-50.00, 
            currency="USD",
            stock_quantity=5,
            assets=json.dumps([]), 
            status="pending_verification"
        ),
        ProductModel(
            id=str(uuid.uuid4()),
            name="Out of Stock Item",
            category="Home",
            price=25.00,
            currency="USD",
            stock_quantity=0, 
            assets=json.dumps(["https://example.com/item.jpg"]),
            status="pending_verification"
        ),
        ProductModel(
            id=str(uuid.uuid4()),
            name="Product Missing Category",
            category="", # Should trigger a 'False' in category_present check
            price=10.00,
            currency="USD",
            stock_quantity=1,
            assets=json.dumps(["https://example.com/item2.jpg"]),
            status="pending_verification"
        )
    ]

    try:
        db.add_all(products)
        db.commit()
        print(f"Successfully seeded {len(products)} products into MySQL using env config!")
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()