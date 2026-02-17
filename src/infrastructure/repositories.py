from sqlalchemy.orm import Session
from sqlalchemy import Column, String, Float, Integer, DateTime, JSON
from sqlalchemy.orm import declarative_base
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import UTC, datetime
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
    created_at = Column(DateTime, default= datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))

class MySQLProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, product_id: str):
        # Fetch the row from the database
        row = self.session.query(ProductModel).filter(ProductModel.id == product_id).first()
        
        if not row:
            return None

        return Product(
            id=row.id,
            name=row.name,
            category=row.category,
            price=row.price,
            currency=row.currency,
            stock_quantity=row.stock_quantity,
            assets=row.assets,
            status=row.status
        )

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
        rows = self.session.query(ProductModel).all()
        return [
            Product(
                id=row.id,
                name=row.name,
                category=row.category,
                price=row.price,
                currency=row.currency,
                stock_quantity=row.stock_quantity,
                assets=row.assets,
                status=row.status
            ) for row in rows
        ]
# MongoDB Model (Audit Log) 
class MongoVerificationRepository:
    def __init__(self, connection_string: str):
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client.verification_db
        self.collection = self.db.verification_logs

    async def log_verification(self, product_id: str, passed: bool, checks: dict,reasons: list):
        document = {
            "product_id": product_id,
            "passed": passed,
            "checks": checks,
            "reasons": reasons,
            "verified_at": datetime.now(UTC)
        }
        await self.collection.insert_one(document)

    async def get_logs_by_product(self, product_id):
        # to_list(length=None) fetches all matching documents
        cursor = self.collection.find({"product_id": product_id}, {"_id": 0})
        return await cursor.to_list(length=100)
    
    async def get_all_logs(self, limit: int = 50, offset: int = 0):
        cursor = self.collection.find({}, {"_id": 0}) \
                                .sort("timestamp", -1) \
                                .skip(offset) \
                                .limit(limit)
        return await cursor.to_list(length=limit)