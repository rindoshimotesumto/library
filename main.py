import asyncio
from email import message
from os import getenv

from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage

from aiogram.enums import ParseMode
from dotenv import load_dotenv
from src.config.logs_conf import logger

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.data.database import Database
from src.data.migrations.runner import run_migrations

from src.bot.middlewares.middlewares import DbMiddleware, CheckSubscriberMiddleware
from src.bot.services.subscribe_service import SubscribeService
from src.bot.handlers import commands, subscribe

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

redis_client = Redis(host='localhost', port=6379, decode_responses=True)
storage = RedisStorage(redis=redis_client)

dp = Dispatcher(storage=storage)
db = Database()

# Run the bot
async def main() -> None:

    if TOKEN is None:
        logger.error("TOKEN not set")
        return

    dp.include_routers(
        commands.router,
        subscribe.router,
    )

    await db.create_db()
    await db.connect()
    await run_migrations(db)

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    sub_service = SubscribeService(bot, db)
    dp.update.outer_middleware(DbMiddleware(db, redis_client))
    dp.callback_query.outer_middleware(CheckSubscriberMiddleware(sub_service))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, redis=redis_client)


if __name__ == "__main__":
    asyncio.run(main())