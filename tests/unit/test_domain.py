import pytest
from src.domain.models import Product

def test_product_verification_passes_with_valid_data():
    product = Product(
        id="123", name="Test", category="Tools", 
        price=10.0, currency="USD", stock_quantity=5, 
        assets=["img.jpg"], status="pending_verification"
    )
    passed, checks = product.evaluate_verification()
    assert passed is True
    assert product.status == "active"

def test_product_verification_fails_with_no_assets():
    product = Product(
        id="123", name="Test", category="Tools", 
        price=10.0, currency="USD", stock_quantity=5, 
        assets=[], status="pending_verification"
    )
    passed, checks = product.evaluate_verification()
    assert passed is False
    assert product.status == "rejected"
    assert checks["has_assets"] is False

def test_product_verification_fails_multiple_reasons():
    # Test a product that fails on almost every rule
    product = Product(
        id="123", 
        name="Bad Product", 
        category="",         # Rule fail: category empty
        price=-10.0,         # Rule fail: price <= 0
        currency="USD", 
        stock_quantity=-1,    # Rule fail: stock < 0
        assets=[],           # Rule fail: no assets
        status="pending_verification"
    )
    
    passed, checks = product.evaluate_verification()
    
    assert passed is False
    assert product.status == "rejected"
    # Verify specific flags are False
    assert checks["category_present"] is False
    assert checks["price_valid"] is False
    assert checks["stock_valid"] is False
    assert checks["has_assets"] is False

def test_product_verification_fails_if_status_not_pending():
    # This ensures our "Guard Clause" works at the domain level
    product = Product(
        id="123", name="Test", category="Tools", 
        price=10.0, currency="USD", stock_quantity=5, 
        assets=["img.jpg"], 
        status="active" # Already active
    )
    
    # Logic should likely return False or raise an error since it's not in the correct state for verification
    passed, checks = product.evaluate_verification()
    assert passed is False