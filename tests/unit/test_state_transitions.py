import pytest
from src.domain.models import Product
from src.application.services import ProductApplicationService

def test_guard_clause_non_pending_status():
    service = ProductApplicationService()
    # If a product is already 'rejected', it shouldn't be evaluated again
    rejected_product = Product(
        name="A", category="B", price=10, currency="USD", 
        stock_quantity=1, assets=["1.jpg"], status="rejected"
    )
    
    # Depending on your implementation, this should either raise an error 
    # or return a specific 'already processed' reason.
    passed, _, reasons = service.evaluate_verification(rejected_product)
    assert "already in rejected state" in reasons[0].lower()