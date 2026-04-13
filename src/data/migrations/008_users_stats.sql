CREATE TABLE IF NOT EXISTS users_stats (
    id SERIAL PRIMARY KEY,

    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,

    liked BOOLEAN DEFAULT FALSE,
    watched INTEGER DEFAULT 0,

    -- Системные поля
    created_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT fk_user_stats_user_id FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_user_stats_book_id FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,

    UNIQUE(user_id, book_id)
);

CREATE INDEX IF NOT EXISTS idx_users_stats_user_id ON users_stats(user_id);