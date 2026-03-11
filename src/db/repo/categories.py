from db.database import DataBase

class CategoriesService():
    def __init__(self, db: DataBase) -> None:
        self.db = db
    
    async def has_categories(self) -> bool:
        sql = "SELECT 1 FROM categories LIMIT 1"
        
        row = await self.db.fetchone(sql)
        return bool(row)
        
    async def get_categories(self, category_id: int | None = None) -> list[dict]:
        sql = """
        SELECT
          category.id AS category_id,
          category.category_name
        FROM categories category
        """
        params = ()

        if category_id:
            min_category_id = await self.get_min_id()
            if category_id == min_category_id["category_id"]:
                sql += """
                    WHERE category.id > ?
                """
            else:
                sql += """
                WHERE category.id < ?
                """
            params = (category_id, )

        sql += "\nORDER BY category.id DESC\nLIMIT 4"
        row = await self.db.fetchall(sql, params)
        return row
        
    async def get_min_id(self) -> dict:
        sql = """
        SELECT
            category.id AS category_id
        FROM categories category
        ORDER BY category.id ASC
        LIMIT 1
        """
        
        row = await self.db.fetchone(sql)
        return row
        
    async def get_max_id(self) -> dict:
        sql = """
        SELECT
            category.id AS category_id
        FROM categories category
        ORDER BY category.id DESC
        LIMIT 1
        """
        
        row = await self.db.fetchone(sql)
        return row