from aiogram import BaseMiddleware
from typing import Callable, Dict, Any
from redis.asyncio import Redis

class DbMiddleware(BaseMiddleware):
    def __init__(self, db):
        self.db = db

    async def __call__(
        self,
        handler: Callable,
        event,
        data: Dict[str, Any]
    ):
        data["db"] = self.db
        return await handler(event, data)