import asyncpg
from typing import Any
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.pool: asyncpg.Pool | None = None
        self.user = getenv("DB_USER", "")
        self.password = getenv("DB_PASSWORD", "")
        self.host = getenv("DB_HOST", "")
        self.db_name = getenv("DB_NAME", "")
        self.port = int(getenv("DB_PORT", "5432"))
        self.min_size = 1
        self.max_size = 5

    async def create_db(self):
        sys_conn = await asyncpg.connect(
            user=self.user, password=self.password, host=self.host, port=self.port, database='postgres'
        )

        exists = await sys_conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", self.db_name
        )

        if not exists:
            await sys_conn.execute(f'CREATE DATABASE "{self.db_name}"')

        await sys_conn.close()

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=self.user,
            password=self.password,
            host=self.host,
            database=self.db_name,
            port=self.port,
            min_size=self.min_size,
            max_size=self.max_size,
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