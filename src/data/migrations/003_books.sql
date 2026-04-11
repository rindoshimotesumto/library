CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,

    -- Основная информация
    title VARCHAR(255) NOT NULL,
    description TEXT,
    language VARCHAR(3) DEFAULT 'uz'
        CHECK (language IN ('uz', 'ru', 'en')),

    -- Навигация и связи
    next_part_id INTEGER DEFAULT NULL,
    category_id INTEGER,                -- Убрал NOT NULL, так как при DELETE SET NULL поле станет пустым
    author_id INTEGER,                  -- Убрал NOT NULL по той же причине

    -- Системные поля
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),

    -- Внешние ключи
    CONSTRAINT fk_next_part FOREIGN KEY (next_part_id) REFERENCES books(id) ON DELETE SET NULL,
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    CONSTRAINT fk_author FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_books_author_id ON books(author_id);
CREATE INDEX IF NOT EXISTS idx_books_category_id ON books(category_id);
CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);