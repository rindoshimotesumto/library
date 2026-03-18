import aiosqlite, sqlite3, os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from typing import Any, Iterable
from src.config.conf_logs import logger

load_dotenv()
backup_dir = os.getenv("BACKUP_DIR", None)

class DataBase:
    def __init__(self, path: str = "src/data/library.sqlite3"):
        self.path = path
        self.conn: aiosqlite.Connection | None = None
        self.backup_path: str = backup_dir

    async def connect(self):
        if self.conn is None:
            self.conn = await aiosqlite.connect(self.path)
            self.conn.row_factory = aiosqlite.Row

            await self.conn.execute("PRAGMA foreign_keys = ON;")
            await self.conn.execute("PRAGMA journal_mode=WAL;")
            await self.conn.execute("PRAGMA synchronous = NORMAL;")
            await self.conn.commit()

        return self.conn

    async def close(self):
        if self.conn:
            await self.conn.close()

    async def executescript(self, script: str):
        conn = await self.connect()

        await conn.executescript(script)
        await conn.commit()

    async def execute(self, query: str, args: Iterable[Any] = ()):
        conn = await self.connect()

        await conn.execute(query, args)
        await conn.commit()

    async def executemany(self, query: str, args: Iterable[Any] = ()):
        conn = await self.connect()

        await conn.executemany(query, args)
        await conn.commit()

    async def backup(self) -> str | None:
        conn = await self.connect()
        if not backup_dir:
            raise ValueError("BACKUP_DIR not set")

        Path(backup_dir).mkdir(parents=True, exist_ok=True)
        filename = datetime.now().strftime("backup_%Y-%m-%d_%H-%M-%S.sqlite3")
        backup_path = str(Path(backup_dir) / filename)

        await conn.commit()
        target = sqlite3.connect(backup_path)

        try:
            await conn.backup(target)
        finally:
            target.close()

        return backup_path

    async def clean_backups(self, keep_last: int = 5):
        path = Path(self.backup_path)
        if not path.exists():
            logger.info("No directory!")
            return

        files = list(path.glob("*.sqlite3"))
        files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

        for old_file in files[keep_last:]:
            logger.info(f"Delete: {old_file}")
            old_file.unlink(missing_ok=True)

    async def fetchone(self, query: str, args: Iterable[Any] = ()):
        conn = await self.connect()

        cur = await conn.execute(query, args)
        row = await cur.fetchone()
        await conn.commit()

        await cur.close()
        return dict(row) if row else None

    async def fetchall(self, query: str, args: Iterable[Any] = ()):
        conn = await self.connect()

        cur = await conn.execute(query, args)
        rows = await cur.fetchall()
        await conn.commit()

        await cur.close()
        return [dict(r) for r in rows]

    async def __aenter__(self):
        return await self.connect()

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()