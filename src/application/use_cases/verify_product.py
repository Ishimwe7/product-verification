from src.domain.models import Product
import datetime

class VerifyProductUseCase:
    def __init__(self, mysql_repo, mongo_repo, service, dispatcher):
        self.mysql_repo = mysql_repo
        self.mongo_repo = mongo_repo
        self.service = service  # Injected Application Service
        self.dispatcher = dispatcher

    async def execute(self, product_id: str):
        # 1. Fetch Entity (Ensure repo returns a Product instance, not a dict)
        product = self.mysql_repo.get_by_id(product_id)
        if not product:
            return None

        if product.status != "pending_verification":
            raise ValueError(f"Product is already {product.status}")

        # 2. Use the Service for logic
        passed, checks, reasons = self.service.evaluate_verification(product)

        # 3. Update Status
        product.status = "active" if passed else "rejected"

        # 4. Persistence
        self.mysql_repo.update_status(product.id, product.status)
        # Pass 'reasons' to Mongo to fulfill Requirement #4
        await self.mongo_repo.log_verification(product.id, passed, checks, reasons)

        # 5. Dispatch Event
        from src.domain.models import ProductVerificationCompleted
        self.dispatcher.dispatch(
            ProductVerificationCompleted(product_id=product.id, status=product.status)
        )

        return product