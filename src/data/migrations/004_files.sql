CREATE TABLE IF NOT EXISTS files (
    id SERIAL PRIMARY KEY,

    -- ID книги которой принадлежат данные
    book_id INTEGER NOT NULL,

    -- Файлы (электронная и аудио-версия)
    file_type VARCHAR(10) DEFAULT 'document'
        CHECK (file_type IN ('document', 'audio', 'cover')),     -- Тип документы, на всякий случай

    telegram_file_id VARCHAR(255) NOT NULL,                 -- ID к файлу от телеграмм
    metadata JSONB DEFAULT '{}'::jsonb,                     -- Данные файла (размер, длительность)

    -- Системные поля
    created_at TIMESTAMP DEFAULT NOW(),                     -- Время добавления в базу

    -- Внешние ключи (Foreign Keys)
    CONSTRAINT fk_files_book_id FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_files_book_id ON files(book_id);