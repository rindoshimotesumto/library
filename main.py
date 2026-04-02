import asyncio
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

from src.bot.middlewares.middlewares import DbMiddleware
from src.bot.handlers import commands

from src.bot.services.cache_service import UserCacheService

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
    )

    await db.connect()
    await run_migrations(db)

    dp.message.middleware(DbMiddleware(db))
    dp.callback_query.middleware(DbMiddleware(db))

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, redis=redis_client)


if __name__ == "__main__":
    asyncio.run(main())