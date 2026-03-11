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
            min_book_id = await self.get_min_id()
            if book_id == min_book_id["book_id"]:
                sql += """
                    WHERE book.id > ?
                """
            else:
                sql += """
                WHERE book.id < ?
                """
            params = (book_id, )

        sql += "\nORDER BY book.id DESC\nLIMIT 4"
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
            book_file.file_id,
            book.cover_file_id
        FROM books book
        JOIN authors author
          ON author.id = book.author_id
        JOIN categories category
          ON category.id = book.category_id
        JOIN book_files book_file
          ON book_file.book_id = book.id
        WHERE book.id = ?
        """

        params = (book_id, )
        row = await self.db.fetchone(sql, params)
        return row

    async def get_book_files(self, book_id: int) -> dict:
        sql = """
        SELECT 
            book.file_id
        FROM book_files book
        WHERE book.book_id = ?
        """

        params = (book_id, )
        row = await self.db.fetchall(sql, params)
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
        
    async def get_min_id(self) -> dict:
        sql = """
        SELECT
            book.id AS book_id
        FROM books book
        ORDER BY book.id ASC
        LIMIT 1
        """
        
        row = await self.db.fetchone(sql)
        return row
        
    async def get_max_id(self) -> dict:
        sql = """
        SELECT
            book.id AS book_id
        FROM books book
        ORDER BY book.id DESC
        LIMIT 1
        """
        
        row = await self.db.fetchone(sql)
        return row
        
    async def search_book(self, book_name: str) -> list[dict]:
        sql = """
        SELECT
            book.id AS book_id,
            book.book_name
        FROM books book
        WHERE book.book_name LIKE ? || '%';
        """
        
        params = (book_name,)
        row = await self.db.fetchall(sql, params)
        
        return row