from typing import Optional

from pydantic import BaseModel
from redis.asyncio import Redis
from src.i18n.i18n import Langs, DEFAULT_LANG

class DefaultUserData(BaseModel):
    tg_id: Optional[int] = None
    lang: str = DEFAULT_LANG.value
    role: str = 'user'

class UserCacheService:
    def __init__(self, redis: Redis):
        self.redis = redis
        self.default_data = DefaultUserData

    async def get_user(self, user_id: int) -> dict:
        key = f"user:{user_id}"
        return await self.redis.hgetall(key)

    async def update_user(self, user_id: int, ttl: int | None = 300, **kwargs) -> None:
        if not kwargs:
            return

        key = f"user:{user_id}"
        async with self.redis.pipeline(transaction=True) as pipe:
            pipe.hset(key, mapping=kwargs)

            if ttl is not None:
                pipe.expire(key, ttl)

            await pipe.execute()

    async def delete_fields(self, user_id: int, *args) -> None:
        if not args:
            return

        key = f"user:{user_id}"
        await self.redis.hdel(key, *args)

    async def delete_user_entirely(self, user_id: int) -> None:
        key = f"user:{user_id}"
        await self.redis.delete(key)