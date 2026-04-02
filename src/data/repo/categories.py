from src.data.database import Database
from src.config.logs_conf import logger

class Category:
    def __init__(self, db: Database):
        self.db = db

    async def search_category(self, category_name: str) -> int:
        sql = """
        SELECT id FROM categories
        WHERE name ILIKE $1 || '%'
        """

        params = [category_name]

        try:
            category_id = await self.db.fetch_val(sql, *params)
            return category_id

        except Exception as e:
            logger.error(e)
            return -1

class AddCategory(Category):
    async def add_category(self, category_name: str) -> int:
        c_search = await self.search_category(category_name)

        if c_search is not None:
            return c_search

        sql = """
        INSERT INTO categories (name)
        VALUES ($1) RETURNING id;
        """

        params = [category_name,]

        try:
            category_id = await self.db.fetch_val(sql, *params)
            return category_id

        except Exception as e:
            logger.error(e)
            return -1

class EditCategory(Category):
    async def edit_category(self, category_id: int, category_name: str) -> int | str:

        c_search = await self.search_category(category_name)

        if c_search is not None and c_search != category_id:
            return -2

        sql = """
        UPDATE categories
        SET name = $1
        WHERE id = $2
        RETURNING name;
        """

        params = [category_name, category_id]

        try:
            category_new_name = await self.db.fetch_val(sql, *params)
            return category_new_name

        except Exception as e:
            logger.error(e)
            return -1

class DeleteCategory(Category):
    async def delete_category(self, category_name: str) -> int:

        c_search = await self.search_category(category_name)

        if c_search is None:
            return -2

        sql = """
        DELETE FROM categories
        WHERE id = $1
        RETURNING id;
        """

        params = [c_search]

        try:
            category_id = await self.db.fetch_val(sql, *params)
            return category_id

        except Exception as e:
            logger.error(e)
            return -1