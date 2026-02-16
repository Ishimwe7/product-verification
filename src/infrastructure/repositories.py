from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Float, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from typing import Optional, Dict, Any
from src.domain.models import Product

Base = declarative_base()

# MySQL Model (Core Record) 
class ProductModel(Base):
    __tablename__ = "products"
    
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)
    stock_quantity = Column(Integer, default=0)
    assets = Column(JSON, nullable=True)
    status = Column(String(50), default="pending_verification") #
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MySQLProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, product_id: str):
        # Fetch the row from the database
        product_row = self.session.query(ProductModel).filter(ProductModel.id == product_id).first()
        
        if not product_row:
            return None

        # Manually map it to a dictionary so the Use Case can find "category"
        return {
            "id": product_row.id,
            "name": product_row.name,
            "category": product_row.category,
            "price": product_row.price,
            "currency": product_row.currency,
            "stock_quantity": product_row.stock_quantity,
            "assets": product_row.assets,  
            "status": product_row.status
        }

    def update_status(self, product_id: str, status: str):
        product = self.session.query(ProductModel).filter(ProductModel.id == product_id).first()
        if product:
            product.status = status
            self.session.commit()
    def save(self, product: Product):
        db_product = ProductModel(
            id=product.id,
            name=product.name,
            category=product.category,
            price=product.price,
            currency=product.currency,
            stock_quantity=product.stock_quantity,
            assets=product.assets,
            status=product.status
        )
        self.session.add(db_product)
        self.session.commit()
        self.session.refresh(db_product)
        
    def get_all(self):
        product_rows = self.session.query(ProductModel).all()
        return [
            {
                "id": row.id,
                "name": row.name,
                "category": row.category,
                "price": row.price,
                "currency": row.currency,
                "stock_quantity": row.stock_quantity,
                "assets": row.assets,
                "status": row.status,
                "created_at": row.created_at
            }
            for row in product_rows
        ]
# MongoDB Model (Audit Log) 
class MongoVerificationRepository:
    def __init__(self, connection_string: str):
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client.verification_db
        self.collection = self.db.verification_logs

    async def log_verification(self, product_id: str, passed: bool, checks: dict):
        document = {
            "product_id": product_id,
            "passed": passed,
            "checks": checks,
            "verified_at": datetime.utcnow()
        }
        await self.collection.insert_one(document)