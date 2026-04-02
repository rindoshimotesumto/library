CREATE TABLE IF NOT EXISTS categories(
    id SERIAL PRIMARY KEY,

    -- Основная информация
    name VARCHAR(100) NOT NULL,

    -- Временные метки (с учетом часового пояса)
    created_at TIMESTAMPTZ DEFAULT NOW(),      -- Время создания
    updated_at TIMESTAMPTZ DEFAULT NOW()       -- Время последнего обновления
);