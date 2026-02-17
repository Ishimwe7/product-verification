from src.domain.models import Product

class ProductApplicationService:
    @staticmethod
    def prepare_for_creation(data: dict) -> Product:
        """
        Ensures the product is initialized in the correct domain state.
        Satisfies Hard Constraint: Status must start as pending_verification.
        """
        return Product(
            name=data.get("name"),
            category=data.get("category"),
            price=data.get("price"),
            currency=data.get("currency"),
            stock_quantity=data.get("stock_quantity", 0),
            assets=data.get("assets", []),
            status="pending_verification"  #
        )

    @staticmethod
    def evaluate_verification(product: Product) -> tuple[bool, dict, list[str]]:
        """
        Pure business logic for Requirement #4.
        Returns: (passed, checks_dict, reasons_list)
        """
        # 1. Defining the specific checks requested
        checks = {
            "name_present": bool(product.name),
            "category_present": bool(product.category),
            "currency_present": bool(product.currency),
            "price_valid": product.price > 0,
            "stock_valid": product.stock_quantity >= 0,
            "has_assets": len(product.assets) >= 1
        }
        
        # 2. Map failures to the 'reasons' required for Mongo
        reasons = []

        if product.status != "pending_verification":
            reasons.append(f"Product is already in {product.status} state")
            return False, {}, reasons
        
        if not checks["name_present"]: reasons.append("Name is required.")
        if not checks["category_present"]: reasons.append("Category is required.")
        if not checks["currency_present"]: reasons.append("Currency code is required.")
        if not checks["price_valid"]: reasons.append("Price must be greater than 0.")
        if not checks["stock_valid"]: reasons.append("Stock cannot be negative.")
        if not checks["has_assets"]: reasons.append("At least one asset is required.")

        passed = all(checks.values())
        
        return passed, checks, reasons