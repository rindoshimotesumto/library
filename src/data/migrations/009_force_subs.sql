CREATE TABLE IF NOT EXISTS mandatory_channels (
    id SERIAL PRIMARY KEY,

    chat_id BIGINT UNIQUE NOT NULL,

    -- название (например, "Канал про крипту")
    title VARCHAR(255) NOT NULL,

    -- Ссылка на канал
    invite_link VARCHAR(255) NOT NULL,

    -- Мягкое удаление / Временное отключение (TRUE - проверяем, FALSE - не проверяем)
    is_active BOOLEAN DEFAULT TRUE,

    -- Системные поля
    created_at TIMESTAMPTZ DEFAULT NOW()
);