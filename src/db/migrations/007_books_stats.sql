CREATE TABLE IF NOT EXISTS books_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    book_id INTEGER NOT NULL,
    book_category_id INTEGER NOT NULL,
    liked INTEGER NOT NULL,
    watched INTEGER NOT NULL,
    read INTEGER NOT NULL,
    listened INTEGER NOT NULL,
    listening INTEGER NOT NULL,
    i_want_to_listen INTEGER NOT NULL,
    downloaded INTEGER NOT NULL,
    
    FOREIGN KEY (book_id)
        REFERENCES books(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
        
    FOREIGN KEY (book_category_id)
        REFERENCES categories(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_book_id
ON books(id);

CREATE INDEX IF NOT EXISTS idx_book_category_id
ON books(category_id);