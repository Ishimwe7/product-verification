from pydantic import BaseModel, Field
from typing import List

class ProductCreateSchema(BaseModel):
    name: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    currency: str = Field(..., min_length=3, max_length=3)
    stock_quantity: int = Field(..., ge=0)
    assets: List[str] = Field(..., min_items=1)

    class Config:
        from_attributes = True