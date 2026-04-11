CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,

    tg_id BIGINT UNIQUE NOT NULL,
    lang VARCHAR(10) DEFAULT 'uz' CHECK (lang IN ('uz', 'ru', 'en')),
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('user', 'admin', 'super admin')),
    is_premium BOOL DEFAULT false,

    -- Системные поля
    created_at TIMESTAMPTZ DEFAULT NOW()                  -- Время добавления в базу
);