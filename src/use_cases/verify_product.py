from src.domain.models import Product
import datetime

class VerifyProductUseCase:
    def __init__(self, mysql_repo, mongo_repo, dispatcher):
        self.mysql_repo = mysql_repo
        self.mongo_repo = mongo_repo
        self.dispatcher = dispatcher

    async def execute(self, product_id: str):
        # 1. Get raw data from MySQL
        data = self.mysql_repo.get_by_id(product_id)
        if not data:
            return None

        # Check the status before doing anything else
        if data["status"] != "pending_verification":
            # Log an audit trail for this attempt
            await self.mongo_repo.log_verification(product_id, False, {"error": f"Product is already in {data['status']} state"})     
            raise ValueError(f"Product is already {data['status']} and cannot be re-verified.")

        product = Product(
            id=data["id"],
            name=data["name"],
            category=data["category"],
            price=data["price"],
            currency=data["currency"],
            stock_quantity=data["stock_quantity"],
            assets=data["assets"], # Ensure this is a list
            status=data["status"]
        )

        # 3. Run the logic we wrote in models.py
        passed, checks = product.evaluate_verification()

        # 4. Save updated status back to MySQL
        self.mysql_repo.update_status(product.id, product.status)

        # 5. Log the audit trail to MongoDB (Requirement #5)
        await self.mongo_repo.log_verification(product.id, passed, checks)

        # 6. Dispatch the completion event
        from src.domain.models import ProductVerificationCompleted
        self.dispatcher.dispatch(
            ProductVerificationCompleted(product_id=product.id, status=product.status)
        )

        return product