CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,

    tg_id BIGINT UNIQUE NOT NULL,

    -- Системные поля
    created_at TIMESTAMP DEFAULT NOW()                  -- Время добавления в базу
);

CREATE INDEX IF NOT EXISTS idx_users_tg_id ON users(tg_id);