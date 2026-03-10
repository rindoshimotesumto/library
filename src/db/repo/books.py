from db.database import DataBase

class BooksService():
    def __init__(self, db: DataBase) -> None:
        self.db = db
    
    async def has_books(self) -> bool:
        sql = "SELECT 1 FROM books LIMIT 1"
        
        row = await self.db.fetchone(sql)
        return bool(row)