import os
import uuid
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.repositories import ProductModel

# 1. Load Environment Variables
load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER", "Admin")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "Password")
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
    
    products = [
        # SCENARIO: Valid Product (Will become 'active')
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
        # SCENARIO: Rule #1 Failure (Price <= 0)
        ProductModel(
            id=str(uuid.uuid4()),
            name="Free Sample (Invalid Price)",
            category="Testing",
            price=0.00, 
            currency="USD",
            stock_quantity=5,
            assets=json.dumps(["https://img.com/sample.png"]), 
            status="pending_verification"
        ),
        # SCENARIO: Rule #2 Failure (Empty Assets)
        ProductModel(
            id=str(uuid.uuid4()),
            name="Product with No Images",
            category="Home",
            price=25.00,
            currency="USD",
            stock_quantity=10, 
            assets=json.dumps([]),
            status="pending_verification"
        ),
        # SCENARIO: Rule #3 Failure (Empty Category)
        ProductModel(
            id=str(uuid.uuid4()),
            name="Ghost Category Item",
            category="", 
            price=10.00,
            currency="USD",
            stock_quantity=1,
            assets=json.dumps(["https://img.com/ghost.png"]),
            status="pending_verification"
        ),
        # SCENARIO: Multiple Rule Failure (Price & Assets)
        ProductModel(
            id=str(uuid.uuid4()),
            name="Total Failure Item",
            category="Testing",
            price=-10.00,
            currency="USD",
            stock_quantity=1,
            assets=json.dumps([]),
            status="pending_verification"
        )
    ]

    try:
        # Check if we already have data to prevent massive bloat
        existing_count = db.query(ProductModel).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} items. Skipping seed.")
            return

        db.add_all(products)
        db.commit()
        print(f"Successfully seeded {len(products)} products into MySQL!")
        print("Tip: Use the Swagger UI to verify these IDs and check the /logs endpoint.")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()