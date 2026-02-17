import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_full_product_lifecycle():
    # 1. CREATE
    product_data = {
        "name": "Integration Test Phone",
        "category": "Mobile",
        "price": 999.0,
        "currency": "USD",
        "stock_quantity": 20,
        "assets": ["https://img.com/phone.png"]
    }
    create_res = client.post("/api/v1/products", json=product_data)
    assert create_res.status_code == 201
    product_id = create_res.json()["id"]

    # 2. VERIFY (The Use Case coordinates MySQL and Mongo here)
    verify_res = client.post(f"/api/v1/products/{product_id}/verify")
    assert verify_res.status_code == 200
    assert verify_res.json()["status"] == "active"

    # 3. GET (Verify persistence in MySQL)
    get_res = client.get(f"/api/v1/products/{product_id}")
    assert get_res.status_code == 200
    assert get_res.json()["status"] == "active"

def test_error_handling_already_verified():
    # Setup: Create and verify
    product_data = {"name": "A", "category": "B", "price": 1, "currency": "USD", "stock_quantity": 10, "assets": ["1"]}
    p_id = client.post("/api/v1/products", json=product_data).json()["id"]
    client.post(f"/api/v1/products/{p_id}/verify") # First time
    
    # Action: Try to verify again
    second_verify = client.post(f"/api/v1/products/{p_id}/verify")
    
    # Assert: Should fail based on your Use Case guard clause
    assert second_verify.status_code == 400
    assert "already" in second_verify.json()["detail"].lower()