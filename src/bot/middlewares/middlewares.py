from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from typing import Callable, Dict, Any

from aiogram.types import User
from redis import Redis

from src.config.logs_conf import logger
from src.bot.services.subscribe_service import SubscribeService
from src.bot.services.cache_service import UserCacheService, DefaultUserData

from src.data.database import Database
from src.i18n.i18n import t, DEFAULT_LANG, Langs
from src.bot.keyboards.inline import check_sub_kb
from src.data.repo.user import UserRepo, UserDataType


class DbMiddleware(BaseMiddleware):
    def __init__(self, db: Database, redis: Redis) -> None:
        self.db = db
        self.redis = redis

    async def __call__(self, handler: Callable, event: TelegramObject, data: Dict[str, Any]):
        user = data.get("event_from_user")
        if not user or user.is_bot:
            return await handler(event, data)

        repo = UserRepo(self.db)
        cache = UserCacheService(self.redis)

        user_data = await cache.get_user(user.id)

        if not user_data:
            db_user = await repo.add_user(
                UserDataType(tg_id=user.id, lang=DEFAULT_LANG.value, role='user')
            )

            user_data = {
                'tg_id': user.id,
                'lang': db_user.lang if db_user else DEFAULT_LANG.value,
                'role': 'user'
            }

            await cache.update_user(user.id, **user_data)

        data["user"] = DefaultUserData(**user_data)
        data["user_repo"] = repo
        data["user_cache"] = cache

        return await handler(event, data)


class CheckSubscriberMiddleware(BaseMiddleware):
    def __init__(self, subscribe_service: SubscribeService) -> None:
        self.service = subscribe_service

    async def __call__(self, handler: Callable, event: Message | CallbackQuery, data: Dict[str, Any]):
        user_obj: User = data.get("event_from_user")

        if not user_obj or user_obj.is_bot:
            return await handler(event, data)

        channels, is_subscribed = await self.service.check_subscribe_status(user_obj.id)

        if is_subscribed:
            return await handler(event, data)

        user_data: DefaultUserData = data.get("user")
        lang = Langs(user_data.lang) if user_data else DEFAULT_LANG

        answer = t("not:subscribe", lang)
        kb = await check_sub_kb(channels, lang)

        if isinstance(event, Message):
            await event.answer(text, reply_markup=kb)

        elif isinstance(event, CallbackQuery):
            if event.data == "check:subscribe":
                answer = t("not:subscribe:show_alert", lang)
                await event.answer(text=answer, show_alert=True)

            else:
                await event.message.answer(answer, reply_markup=kb)

        return None