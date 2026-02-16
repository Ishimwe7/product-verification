from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid

@dataclass(kw_only=True)
class DomainEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    occurred_at: datetime = field(default_factory=datetime.utcnow)

@dataclass(kw_only=True)
class ProductCreatedPendingVerification(DomainEvent):
    product_id: str

@dataclass(kw_only=True)
class ProductVerificationCompleted(DomainEvent):
    product_id: str
    status: str

class Product:
    def __init__(self, name: str, category: str, price: float, currency: str, 
                 stock_quantity: int, assets: List[str], id: str = None, 
                 status: str = "pending_verification"):
        self.id = id or str(uuid.uuid4())
        self.name = name
        self.category = category
        self.price = price
        self.currency = currency
        self.stock_quantity = stock_quantity
        self.assets = assets
        self.status = status
        self.events = []

    def verify(self, checklist: dict):
        # Verification Logic (Requirement #4)
        is_valid = all([
            len(self.name) > 0,
            len(self.category) > 0,
            len(self.currency) > 0,
            self.price > 0,
            self.stock_quantity >= 0,
            len(self.assets) >= 1
        ])

        self.status = "active" if is_valid else "rejected"
        self.events.append(ProductVerificationCompleted(self.id, self.status))
        return is_valid
    def evaluate_verification(self) -> bool:
        #check if already verified
        if self.status != "pending_verification":
            return False, {"error": f"Product is already in {self.status} state"}
        
        checks = {
            "name_present": bool(self.name),
            "category_present": bool(self.category),
            "currency_present": bool(self.currency),
            "price_valid": self.price > 0,
            "stock_valid": self.stock_quantity >= 0,
            "has_assets": len(self.assets) >= 1
        }
        
        passed = all(checks.values())
        
        if passed:
            self.status = "active"
        else:
            self.status = "rejected"
            
        return passed, checks