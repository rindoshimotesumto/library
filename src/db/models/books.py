from dataclasses import dataclass


@dataclass(slots=True)
class Books:
    book_name: str
    author_id: int
    description: str
    file_id: str
    category_id: int
    pages: int
    language: str
