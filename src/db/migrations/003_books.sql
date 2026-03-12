CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    cover_file_id TEXT NOT NULL,
    book_name TEXT NOT NULL,
    description TEXT NOT NULL,
    year_of_publication INTEGER NOT NULL CHECK (year_of_publication > 0),
    weight INTEGER NOT NULL CHECK (weight > 0),
    language TEXT NOT NULL,
    rating REAL NOT NULL CHECK (rating BETWEEN 0 AND 5),

    UNIQUE(author_id, book_name),

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