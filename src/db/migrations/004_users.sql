CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    tg_id INTEGER NOT NULL UNIQUE,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    
    role TEXT NOT NULL DEFAULT 'user' CHECK(role IN ('user', 'admin')),

    language TEXT DEFAULT 'uz'
);