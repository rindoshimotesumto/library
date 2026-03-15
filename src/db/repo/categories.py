
class CategoriesRepository:
    def __init__(self, db):
        self.db = db

    async def add_category(self, category_name: str):
        sql = """
        INSERT INTO categories (category_name) VALUES (?)
        """

        params = (category_name,)
        await self.db.execute(sql, params)

    async def get_categories(self,  last_id: int | None = None, PAGE_SIZE: int = 9):
        sql = """
        SELECT categories.id, categories.category_name
            FROM categories
        """
        params = []

        if last_id:
            sql += "WHERE categories.id < ?"
            params.append(last_id)

        sql += "ORDER BY categories.id DESC LIMIT ?"
        params.append(PAGE_SIZE)

        row = await self.db.fetchall(sql, tuple(params))
        return row

    async def get_category_id(self, min_: bool) -> int:
        sql = """
        SELECT categories.id FROM categories
        ORDER BY categories.id
        """

        if min_:
            sql += """ LIMIT 1"""
        else:
            sql += """DESC LIMIT 1"""

        row = await self.db.fetchone(sql)
        return row["id"]