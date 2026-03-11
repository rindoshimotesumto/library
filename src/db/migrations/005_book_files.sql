CREATE TABLE IF NOT EXISTS book_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    book_id INTEGER NOT NULL,
    file_id TEXT NOT NULL,
    
    FOREIGN KEY (book_id)
        REFERENCES books(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_book_id
ON books(id);