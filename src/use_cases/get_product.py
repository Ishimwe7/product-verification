class GetProductUseCase:
    def __init__(self, mysql_repo):
        self.mysql_repo = mysql_repo

    def execute(self, product_id: str):
        product_data = self.mysql_repo.get_by_id(product_id)
        
        if not product_data:
            return None
            
        return product_data