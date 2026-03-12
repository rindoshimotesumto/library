from dataclasses import dataclass
from sqlite3.dbapi2 import paramstyle
from typing import Optional


@dataclass
class Book:
    category_id: int
    author_id: int
    cover_file_id: str
    book_name: str
    description: str
    year_of_publication: int
    weight: int
    language: str
    rating: float
    id: Optional[int] = None


class BookRepository:
    def __init__(self, db):
        self.db = db

    async def add_book(self, book: Book) -> int:
        sql = """
        INSERT INTO books (category_id, author_id, cover_file_id, book_name,
                            description, year_of_publication, weight, language, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING id
        """

        params = (
            book.category_id, book.author_id, book.cover_file_id,
            book.book_name, book.description, book.year_of_publication,
            book.weight, book.language, book.rating
        )

        result = await self.db.fetchone(sql, params)

        inserted_id = result['id']
        book.id = inserted_id

        return inserted_id

    async def get_book(self, book_id: int) -> Book | None:
        sql = """
        SELECT id,
               category_id,
               author_id,
               cover_file_id,
               book_name,
               description,
               year_of_publication,
               weight, language, rating
        FROM books
        WHERE id = ?
        """

        row = await self.db.fetchone(sql, (book_id,))

        if row:
            return Book(**row)

        return None

    async def get_books(self,  last_id: int | None = None, PAGE_SIZE: int = 50):
        sql = """
        SELECT books.id, books.book_name
            FROM books
        """
        params = []

        if last_id:
            sql += "WHERE books.id > ?"
            params.append(last_id)

        sql += "ORDER BY books.id DESC LIMIT ?"
        params.append(PAGE_SIZE)

        row = await self.db.fetchall(sql, tuple(params))
        return row

    async def get_books_category(self,  category_id: int, last_id: int | None = None, PAGE_SIZE: int = 50):
        sql = """
        SELECT books.id, books.book_name
            FROM books
        """
        params = [category_id]

        if last_id:
            sql += "WHERE books.id > ? AND books.category_id = ?"
            params.append(last_id)

        sql += "ORDER BY books.id DESC LIMIT ?"
        params.append(PAGE_SIZE)

        row = await self.db.fetchall(sql, tuple(params))
        return row

    async def add_book_file(self, book_id: int, book_file_id: str):
        sql = """
        INSERT INTO book_files (book_id, file_id)
            VALUES (?, ?)
        """

        params = (book_id, book_file_id)
        await self.db.execute(sql, params)