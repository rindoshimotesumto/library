import aiosqlite
from typing import Any, Iterable


class DataBase:
    def __init__(self, path: str = "src/data/library.sqlite3"):
        self.path = path
        self.conn: aiosqlite.Connection | None = None

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