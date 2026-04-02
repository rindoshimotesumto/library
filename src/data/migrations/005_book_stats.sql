CREATE TABLE IF NOT EXISTS book_stats (
    id SERIAL PRIMARY KEY,


    book_id INTEGER UNIQUE NOT NULL,

    -- Статистика конкретной книги:
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    rating NUMERIC(3, 2) DEFAULT 0.00,

    CONSTRAINT fk_stats_book_id FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);