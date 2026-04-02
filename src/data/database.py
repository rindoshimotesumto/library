import asyncpg
from typing import Any
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.pool: asyncpg.Pool | None = None

    async def connect(self):
        # noinspection PyTypeChecker
        self.pool = await asyncpg.create_pool(
            user=getenv("DB_USER", ""),
            password=getenv("DB_PASSWORD", ""),
            host=getenv("DB_HOST", ""),
            database=getenv("DB_NAME", ""),
            port=int(getenv("DB_PORT", "5432")),
            min_size=1,
            max_size=5
        )

    async def close(self):
        if self.pool is not None:
            await self.pool.close()
            
    async def execute(self, query: str, *args) -> str:
        return await self.pool.execute(query, *args)

    async def execute_many(self, query: str, args: list[tuple]) -> None:
        await self.pool.executemany(query, args)

    async def fetch_all(self, query: str, *args) -> list[asyncpg.Record]:
        return await self.pool.fetch(query, *args)

    async def fetch_one(self, query: str, *args) -> asyncpg.Record | None:
        return await self.pool.fetchrow(query, *args)

    async def fetch_val(self, query: str, *args) -> Any:
        return await self.pool.fetchval(query, *args)