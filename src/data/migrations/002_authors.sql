CREATE TABLE IF NOT EXISTS authors (
    id SERIAL PRIMARY KEY,

    -- Основная информация
    name VARCHAR(100) NOT NULL,             -- Имя автора
    created_at TIMESTAMP DEFAULT NOW()      -- Время добавления в базу
);