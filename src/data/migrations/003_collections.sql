CREATE TABLE IF NOT EXISTS collections (
    id SERIAL PRIMARY KEY,

    -- Основная информация
    name VARCHAR(255) NOT NULL,
    description TEXT,

    -- Навигация и связи
    author_id INT DEFAULT NULL,

    -- Системные поля
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT fk_author FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE SET NULL
);

-- Индексы
CREATE INDEX IF NOT EXISTS idx_collections_id ON collections(id);