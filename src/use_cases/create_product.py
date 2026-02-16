import uuid
from src.domain.models import Product

class CreateProductUseCase:
    def __init__(self, mysql_repo, dispatcher):
        """
        Injected dependencies.
        """
        self.mysql_repo = mysql_repo
        self.dispatcher = dispatcher

    def execute(self, data: dict) -> Product:
        # 1. Create the Domain Entity
        # Requirement #6: Status must start as 'pending_verification'
        product = Product(
            id=str(uuid.uuid4()),
            name=data['name'],
            category=data['category'],
            price=data['price'],
            currency=data['currency'],
            stock_quantity=data['stock_quantity'],
            assets=data['assets'],
            status="pending_verification" 
        )

        # 2. Persist to MySQL
        self.mysql_repo.save(product)

        # 3. Dispatch Domain Event
        # This helps with the event-driven requirement
        #self.dispatcher.dispatch({"event": "ProductCreated", "id": product.id})
        from src.domain.models import ProductCreatedPendingVerification

        self.dispatcher.dispatch(
            ProductCreatedPendingVerification(product_id=product.id)
        )

        return product