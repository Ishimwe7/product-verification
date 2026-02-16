class ListProductsUseCase:
    def __init__(self, mysql_repo):
        self.mysql_repo = mysql_repo

    def execute(self):
        products = self.mysql_repo.get_all()
        
        # If the list is empty, we return None or raise an error
        if not products:
            return None
            
        return products