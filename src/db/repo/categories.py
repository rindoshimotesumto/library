import math

class CategoriesRepository:
    def __init__(self, db):
        self.db = db

    async def add_category(self, category_name: str):
        sql = """
        INSERT INTO categories (category_name) VALUES (?)
        """

        params = (category_name,)
        await self.db.execute(sql, params)

    async def get_categories(
            self,
            cursor_id: int | None = None,
            page_size: int = 9,
            direction: str = "next",
            admin: bool = False,
    ):
        if cursor_id is None:
            sql = """
            SELECT categories.id, categories.category_name
            """

            if admin:
                sql += """
                        , COUNT(books.id) as book_count
                    FROM categories
                        JOIN books ON categories.id = books.category_id
                    GROUP BY categories.id, categories.category_name
                    ORDER BY categories.id DESC
                    LIMIT ?
                """

            else:
                sql += """
                    FROM categories
                    ORDER BY categories.id DESC
                    LIMIT ?
                """

            return await self.db.fetchall(sql, (page_size,))

        if direction == "next":
            sql = """
            SELECT categories.id, categories.category_name
            """

            if admin:
                sql += """
                        , COUNT(books.id) as book_count
                    FROM categories
                        JOIN books ON categories.id = books.category_id
                    WHERE categories.id < ?
                    GROUP BY categories.id, categories.category_name
                    ORDER BY categories.id DESC
                    LIMIT ?
                """

            else:
                sql += """
                    FROM categories
                    WHERE categories.id < ?
                    ORDER BY categories.id DESC
                    LIMIT ?
                """

            return await self.db.fetchall(sql, (cursor_id, page_size))

        if direction == "prev":
            sql = """
            SELECT categories.id, categories.category_name
            """

            if admin:
                sql += """
                    , COUNT(books.id) as book_count
                    FROM categories
                        JOIN books ON categories.id = books.category_id
                    WHERE categories.id > ?
                    GROUP BY categories.id, categories.category_name
                    ORDER BY categories.id ASC
                    LIMIT ?
                """

            else:
                sql += """
                    FROM categories
                    WHERE categories.id > ?
                    ORDER BY categories.id ASC
                    LIMIT ?    
                """

            rows = await self.db.fetchall(sql, (cursor_id, page_size))
            return list(reversed(rows))

        raise ValueError(f"Unknown direction: {direction}")

    async def get_categories_page_count(self, page_size: int = 9):
        sql = """
        SELECT COUNT(*) as count
        FROM categories
        """
        row = await self.db.fetchone(sql)
        return max(1, math.ceil(row["count"] / page_size))

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

    async def edit_category(self, name: str, c_id: int):
        sql = """
        UPDATE categories SET category_name = ? WHERE id = ?
        """
        params = (name, c_id)
        await self.db.execute(sql, params)