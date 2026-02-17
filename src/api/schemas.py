from pydantic import BaseModel, Field, ConfigDict
from typing import List

class ProductCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True) 

    name: str 
    category: str 
    price: float 
    currency: str 
    stock_quantity: int 
    assets: List[str] 