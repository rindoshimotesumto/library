from dataclasses import dataclass
from sqlite3.dbapi2 import paramstyle
from typing import Optional


@dataclass
class Book:
    category_id: int
    book_file_link: str
    cover_file_id: str
    book_name: str
    author_id: int
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
        INSERT INTO books (category_id, author_id, book_file_link, cover_file_id, book_name,
                            description, year_of_publication, weight, language, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING id
        """

        params = (
            book.category_id, book.author_id, book.book_file_link, book.cover_file_id,
            book.book_name, book.description, book.year_of_publication,
            book.weight, book.language, book.rating
        )

        result = await self.db.fetchone(sql, params)

        inserted_id = result['id']
        book.id = inserted_id

        return inserted_id

    async def get_book(self, book_id: int) -> Book | None:
        sql = """
        SELECT 
            books.id,
            books.category_id,
            books.book_file_link,
            books.cover_file_id,
            books.book_name,
            authors.author_name AS author_id,
            books.description,
            books.year_of_publication,
            books.weight, language, rating
        FROM books
        JOIN authors
            ON books.author_id = authors.id
        WHERE books.id = ?
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

        sql += """
        WHERE books.category_id = ?
        ORDER BY books.id DESC LIMIT ?
        """
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