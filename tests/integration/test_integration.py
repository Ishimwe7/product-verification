import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_full_product_lifecycle():
    # 1. CREATE: Post a new product
    product_data = {
        "name": "Integration Test Camera",
        "category": "Electronics",
        "price": 500.0,
        "currency": "USD",
        "stock_quantity": 10,
        "assets": ["https://example.com/photo.jpg"]
    }
    create_response = client.post("/api/v1/products", json=product_data)
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]
    assert create_response.json()["status"] == "pending_verification"

    # 2. VERIFY: Trigger the verification process
    verify_response = client.post(f"/api/v1/products/{product_id}/verify")
    assert verify_response.status_code == 200
    assert verify_response.json()["status"] == "active"

    # 3. RETRIEVE: Ensure the status is updated and saved
    get_response = client.get(f"/api/v1/products/{product_id}")
    assert get_response.status_code == 200
    assert get_response.json()["status"] == "active"

def test_verify_non_existent_product():
    # Test error handling
    response = client.post("/api/v1/products/non-existent-id/verify")
    assert response.status_code == 404

def test_get_all_products():
    # 1. Ensure we have at least one product (relying on seed or previous test)
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_get_single_product_with_details():
    # 1. Create a product to ensure it exists
    product_data = {
        "name": "Detail Test Item",
        "category": "Testing",
        "price": 99.99,
        "currency": "USD",
        "stock_quantity": 5,
        "assets": ["https://example.com/item.jpg"]
    }
    create_res = client.post("/api/v1/products", json=product_data)
    product_id = create_res.json()["id"]

    # 2. Get that specific product
    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Detail Test Item"
    assert "status" in data