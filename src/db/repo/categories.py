from db.database import DataBase

class CategoriesService():
    def __init__(self, db: DataBase) -> None:
        self.db = db
    
    async def has_categories(self) -> bool:
        sql = "SELECT 1 FROM categories LIMIT 1"
        
        row = await self.db.fetchone(sql)
        return bool(row)