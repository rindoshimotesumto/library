import math

from dataclasses import dataclass
from sqlite3 import IntegrityError
from typing import Optional
from zipapp import create_archive
from src.db.database import DataBase

from src.config.conf_logs import logger


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
    def __init__(self, db: DataBase):
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

    async def get_books(self,  last_id: int | None = None, page_size: int = 10):
        sql = """
        SELECT books.id, books.book_name
            FROM books
        """
        params = []

        if last_id:
            sql += "WHERE books.id < ?"
            params.append(last_id)

        sql += "ORDER BY books.id DESC LIMIT ?"
        params.append(page_size)

        row = await self.db.fetchall(sql, tuple(params))
        return row

    async def get_books_category(
            self,
            category_id: int,
            cursor_id: int | None = None,
            page_size: int = 10,
            direction: str = "next",
    ):
        if cursor_id is None:
            sql = """
            SELECT books.id, books.book_name
            FROM books
            WHERE books.category_id = ?
            ORDER BY books.id DESC
            LIMIT ?
            """
            return await self.db.fetchall(sql, (category_id, page_size))

        if direction == "next":
            sql = """
            SELECT books.id, books.book_name
            FROM books
            WHERE books.category_id = ? AND books.id < ?
            ORDER BY books.id DESC
            LIMIT ?
            """
            return await self.db.fetchall(sql, (category_id, cursor_id, page_size))

        if direction == "prev":
            sql = """
            SELECT books.id, books.book_name
            FROM books
            WHERE books.category_id = ? AND books.id > ?
            ORDER BY books.id ASC
            LIMIT ?
            """
            rows = await self.db.fetchall(sql, (category_id, cursor_id, page_size))
            return list(reversed(rows))

        raise ValueError(f"Unknown direction: {direction}")

    async def add_book_file(self, book_id: int, book_file_id: str):
        sql = """
        INSERT INTO book_files (book_id, file_id)
            VALUES (?, ?)
        """

        params = (book_id, book_file_id)
        await self.db.execute(sql, params)

    async def get_books_page_count(self, category_id: int = None, page_book_count: int = 9) -> int:
        sql = """
        SELECT COUNT(*) AS count FROM books
        """
        params = []

        if isinstance(category_id, int):
            sql += " WHERE books.category_id = ?"
            params.append(category_id)

        row = await self.db.fetchone(sql, (*params,))
        return math.ceil(max(row['count'], 1) / page_book_count)
    
    async def change_link(self, channel_username: str = "Railway_kutubxona") -> None:
        rows = await self.db.fetchall("SELECT id, book_file_link FROM books")

        for row in rows:
            book_id = row["id"]
            old_link = row["book_file_link"]

            new_link = old_link.replace(
                old_link.split("/")[-3],
                channel_username
            ).removeprefix("https://t.me/c/")
            
            new_link = "https://t.me/" + new_link

            await self.db.execute(
                "UPDATE books SET book_file_link = ? WHERE id = ?",
                (new_link, book_id)
            )

        return None

    async def update_book_name(self, book_id: int, book_name: str) -> bool:
        sql = """
        UPDATE books SET book_name = ? WHERE id = ?
        """

        try:
            await self.db.execute(sql, (book_name, book_id))
            return True

        except Exception as e:
            logger.error(e)
            return False