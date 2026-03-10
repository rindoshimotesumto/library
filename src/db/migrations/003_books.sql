CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    book_name TEXT NOT NULL UNIQUE,
    author_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    cover_file_id TEXT NOT NULL,
    book_file_id TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    pages INTEGER NOT NULL,
    language TEXT NOT NULL,

    FOREIGN KEY (author_id)
        REFERENCES authors(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
        
    FOREIGN KEY (category_id)
        REFERENCES categories(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_books_author_id
ON books(author_id);

CREATE INDEX IF NOT EXISTS idx_books_category_id
ON books(category_id);