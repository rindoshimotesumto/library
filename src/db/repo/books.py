from db.database import DataBase

class BooksService():
    def __init__(self, db: DataBase) -> None:
        self.db = db
    
    async def has_books(self) -> bool:
        sql = "SELECT 1 FROM books LIMIT 1"
        
        row = await self.db.fetchone(sql)
        return bool(row)

    async def get_books(self, book_id: int | None = None) -> list[dict]:
        sql = """
        SELECT
          book.id AS book_id,
          book.book_name || ' - ' || author.author_name as book_name
        FROM books book
        JOIN authors author
          ON author.id = book.author_id
        """

        params = ()

        if book_id:
            sql += """
            WHERE book.id < ?
            """
            params = (book_id, )

        sql += "\nORDER BY book.id DESC\nLIMIT 3"
        row = await self.db.fetchall(sql, params)
        return row

    async def get_book(self, book_id: int) -> dict:
        sql = """
        SELECT 
            category.category_name,
            author.author_name,
            book.id,
            book.book_name,
            book.description,
            book.book_file_id,
            book.cover_file_id
        FROM books book
        JOIN authors author
          ON author.id = book.author_id
        JOIN categories category
          ON category.id = book.category_id
        WHERE book.id = ?
        """

        params = (book_id, )
        row = await self.db.fetchone(sql, params)
        return row

    async def get_book_file(self, book_id: int) -> dict:
        sql = """
        SELECT 
            book.book_file_id
        FROM books book
        WHERE book.id = ?
        """

        params = (book_id, )
        row = await self.db.fetchone(sql, params)
        return row

    async def get_books_count(self) -> dict:
        sql = """
        SELECT
            sqlite_sequence.seq AS books_count
        FROM sqlite_sequence
        WHERE sqlite_sequence.name = 'books'
        """

        rows = await self.db.fetchone(sql)
        return rows