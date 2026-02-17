import os
from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.repositories import MySQLProductRepository, MongoVerificationRepository, Base
from src.infrastructure.dispatcher import DummyEventDispatcher
from src.application.use_cases.create_product import CreateProductUseCase
from src.application.use_cases.verify_product import VerifyProductUseCase
from src.application.use_cases.get_product import GetProductUseCase
from src.api.schemas import ProductCreateSchema
from src.application.use_cases.list_products import ListProductsUseCase 
from src.application.services import ProductApplicationService
# 1. Database Setup

# Load the .env file
load_dotenv()

# Build MySQL URL from environment variables
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")

MYSQL_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# Build MongoDB URL
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_URL = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"

engine = create_engine(MYSQL_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine) # Creates tables in Docker MySQL

app = FastAPI(title="Product Verification Service")

# Initialize the service once
app_service = ProductApplicationService()

# 2. Dependency Injection Providers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_dispatcher():
    return DummyEventDispatcher()

def get_mongo_repo():
    return MongoVerificationRepository(MONGO_URL)

def get_mysql_repo(db=Depends(get_db)):
    return MySQLProductRepository(db)

def get_create_use_case(db=Depends(get_db), dispatcher=Depends(get_dispatcher)):
    return CreateProductUseCase(mysql_repo=MySQLProductRepository(db), service=app_service, dispatcher=dispatcher)

def get_verify_use_case(db=Depends(get_db), mongo=Depends(get_mongo_repo), dispatcher=Depends(get_dispatcher)):
    # Passing the service into the Use Case
    return VerifyProductUseCase(MySQLProductRepository(db), mongo, app_service, dispatcher)

def get_get_product_use_case(repo=Depends(get_mysql_repo)):
    return GetProductUseCase(repo)

def get_list_products_use_case(repo=Depends(get_mysql_repo)):
    return ListProductsUseCase(repo)

# Endpoints
@app.post("/api/v1/products", status_code=201)
def create_product(payload: ProductCreateSchema, use_case: CreateProductUseCase = Depends(get_create_use_case)):
    product = use_case.execute(payload.model_dump())
    return {"id": product.id, "status": product.status}


@app.post("/api/v1/products/{product_id}/verify")
async def verify_product(product_id: str, use_case: VerifyProductUseCase = Depends(get_verify_use_case)):
    try:
        product = await use_case.execute(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"id": product.id, "status": product.status}
    except ValueError as e:
        # This turns the logic error into a proper 400 Bad Request
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/products/{product_id}")
def get_product(product_id: str, use_case: GetProductUseCase = Depends(get_get_product_use_case)):
    product_data = use_case.execute(product_id)
    if not product_data:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_data

@app.get("/api/v1/products")
def list_products(use_case: ListProductsUseCase = Depends(get_list_products_use_case)):
    products = use_case.execute()
    
    if products is None:
        # Returning a 404 with a custom message
        raise HTTPException(
            status_code=404, 
            detail="No products found in the database. Please seed the database first."
        )
        
    return products

@app.get("/api/v1/products/{product_id}/logs")
async def get_product_logs(product_id: str, repo: MongoVerificationRepository = Depends(get_mongo_repo)):
    logs = await repo.get_logs_by_product(product_id)
    return logs

@app.get("/api/v1/admin/logs")
async def list_all_verification_logs(
    #setting limit to get only 50 last logs
    limit: int = 50, 
    offset: int = 0,
    repo: MongoVerificationRepository = Depends(get_mongo_repo)):
    """
    Admin only: Retrieve all product verification failure/success logs.
    """
    return await repo.get_all_logs(limit,offset)