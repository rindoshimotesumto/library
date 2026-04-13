CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,

    -- Основная информация
    cover_id TEXT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    language VARCHAR(3) DEFAULT 'uz'
        CHECK (language IN ('uz', 'ru', 'en')),

    year_of_publication INT,
    number_of_pages INT DEFAULT NULL,
    weight INT DEFAULT NULL,

    -- Навигация и связи
    next_part_id INTEGER DEFAULT NULL,
    category_id INTEGER,
    author_id INTEGER,
    collection_id INTEGER DEFAULT NULL,

    -- (добавил, потому что есть в FSM)
    link TEXT,

    -- Системные поля
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),

    -- Внешние ключи
    CONSTRAINT fk_next_part FOREIGN KEY (next_part_id) REFERENCES books(id) ON DELETE SET NULL,
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    CONSTRAINT fk_author FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE SET NULL,
    CONSTRAINT fk_collection FOREIGN KEY (collection_id) REFERENCES collections(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_books_author_id ON books(author_id);
CREATE INDEX IF NOT EXISTS idx_books_category_id ON books(category_id);
CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
CREATE INDEX IF NOT EXISTS idx_books_collection_id ON books(collection_id);