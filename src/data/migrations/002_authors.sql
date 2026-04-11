CREATE TABLE IF NOT EXISTS authors (
    id SERIAL PRIMARY KEY,

    -- Основная информация
    name VARCHAR(100) NOT NULL,             -- Имя автора
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()      -- Время добавления в базу
);