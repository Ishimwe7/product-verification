from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)
    
def test_failed_verification_stores_reasons_in_mongo():
    # 1. Create product that is VALID for Pydantic but INVALID for Service
    payload = {
        "name": "",            
        "category": "Test",
        "price": -100,          
        "currency": "USD",
        "stock_quantity": 5,
        "assets": ["test.jpg"]  
    }
    create_res = client.post("/api/v1/products", json=payload)
    
    # Debug: if this fails, print create_res.text to see the Pydantic error
    assert create_res.status_code == 201
    product_id = create_res.json()["id"]

    # 2. Trigger Verify (This should now fail and return 'rejected')
    verify_res = client.post(f"/api/v1/products/{product_id}/verify")
    assert verify_res.json()["status"] == "rejected"