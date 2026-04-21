
class AuthorRepository:
    def __init__(self, db):
        self.db = db

    async def add_author(self, author_name: str):
        sql = """
        INSERT INTO authors (author_name) VALUES (?)
        """

        params = (author_name,)
        await self.db.execute(sql, params)

    async def get_author(self, author_id: int) -> dict:
        sql = "SELECT author_name FROM authors WHERE id = ?"
        params = (author_id,)

        row = await self.db.fetchone(sql, tuple(params))
        return row

    async def get_authors(
            self,
            cursor_id: int | None = None,
            page_size: int = 10,
            direction: str = "next"
    ) -> list[dict]:
        sql = "SELECT * FROM authors"
        params = []

        if cursor_id:
            if direction == "next":
                sql += " WHERE id < ?"
            else:
                sql += " WHERE id > ?"
            params.append(cursor_id)

        order = "DESC" if direction == "next" else "ASC"
        sql += f" ORDER BY id {order} LIMIT ?"
        params.append(page_size)

        rows = await self.db.fetchall(sql, tuple(params))

        # если идём назад — переворачиваем
        if direction == "prev":
            rows = list(reversed(rows))

        return rows

    async def get_authors_page_count(self, page_size: int) -> int:
        sql = "SELECT COUNT(*) as count FROM authors"
        row = await self.db.fetchone(sql)

        total = row["count"]
        return (total + page_size - 1) // page_size


    async def delete_author(self, author_id: int) -> bool:
        sql = "DELETE FROM authors WHERE id = ?"
        result = await self.db.execute(sql, (author_id,))
        return True
