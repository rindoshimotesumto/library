CREATE TABLE IF NOT EXISTS user_book_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INTEGER NOT NULL,

    book_id INTEGER,
    book_category_id INTEGER,
    liked INTEGER DEFAULT 0,
    watched INTEGER DEFAULT 0,
    read INTEGER DEFAULT 0,
    listened INTEGER DEFAULT 0,
    listening INTEGER DEFAULT 0,
    i_want_to_listen INTEGER DEFAULT 0,
    downloaded INTEGER DEFAULT 0,

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