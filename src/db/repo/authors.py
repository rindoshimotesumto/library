
class AuthorRepository:
    def __init__(self, db):
        self.db = db

    async def add_author(self, author_name: str):
        sql = """
        INSERT INTO authors (author_name) VALUES (?)
        """

        params = (author_name,)
        await self.db.execute(sql, params)

    async def get_authors(self, last_id: int | None = None, page_size: int = 10) -> list[dict]:
        sql = """
        SELECT * FROM authors
        """
        params = []

        if last_id:
            params.append(last_id)
            sql += f" WHERE authors.id < ?"

        params.append(page_size)
        sql += f"LIMIT ?"

        row = await self.db.fetchall(sql, tuple(params))
        return row