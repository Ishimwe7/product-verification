import pytest
from src.domain.models import Product
from src.application.services import ProductApplicationService

def test_requirement_4_rules():
    service = ProductApplicationService()
    
    # 1. Test Fail: Negative Price & Missing Assets (Requirement #4)
    bad_product = Product(
        name="Test", category="Tools", price=-10.0, 
        currency="USD", stock_quantity=5, assets=[]
    )
    passed, checks, reasons = service.evaluate_verification(bad_product)
    
    assert passed is False
    assert "Price must be greater than 0." in reasons
    assert "At least one asset is required." in reasons
    assert checks["price_valid"] is False

    # 2. Test Pass: All Requirement #4 rules met
    good_product = Product(
        name="Camera", category="Tech", price=500.0, 
        currency="USD", stock_quantity=10, assets=["img.jpg"]
    )
    passed, _, _ = service.evaluate_verification(good_product)
    assert passed is True