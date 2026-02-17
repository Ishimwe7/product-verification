import uuid
from src.domain.models import Product

class CreateProductUseCase:
    def __init__(self, mysql_repo, service, dispatcher):
        self.mysql_repo = mysql_repo
        self.service = service
        self.dispatcher = dispatcher

    def execute(self, data: dict):
        # Use Service to create the Domain Entity
        # This ensures it starts as 'pending_verification'
        product = self.service.prepare_for_creation(data)
        
        self.mysql_repo.save(product)
        
        # Dispatch the required event
        from src.domain.models import ProductCreatedPendingVerification
        self.dispatcher.dispatch(ProductCreatedPendingVerification(product_id=product.id))
        
        return product