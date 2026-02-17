import pytest
from src.domain.models import Product
from src.application.services import ProductApplicationService

@pytest.fixture
def service():
    return ProductApplicationService()

def test_service_verification_passes_with_valid_data(service):
    product = Product(
        name="Valid Camera", category="Electronics", price=100.0, 
        currency="USD", stock_quantity=5, assets=["image.jpg"]
    )
    
    passed, checks, reasons = service.evaluate_verification(product)
    
    assert passed is True
    assert product.status == "pending_verification" # Service shouldn't mutate yet
    assert len(reasons) == 0

def test_service_verification_fails_multiple_requirements(service):
    product = Product(
        name="", category="", price=-50.0, 
        currency="USD", stock_quantity=-1, assets=[]
    )
    
    passed, checks, reasons = service.evaluate_verification(product)
    
    assert passed is False
    assert "Name is required." in reasons
    assert "Price must be greater than 0." in reasons
    assert "Stock cannot be negative." in reasons
    assert "At least one asset is required." in reasons
    assert checks["has_assets"] is False

def test_service_creation_prep_sets_default_status(service):
    data = {"name": "New Item", "category": "Test", "price": 10.0, "currency": "USD", "assets": []}
    product = service.prepare_for_creation(data)
    
    assert product.status == "pending_verification" # Fulfills Hard Constraint