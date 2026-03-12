import asyncio
from os import getenv

from aiogram.enums import ParseMode
from dotenv import load_dotenv
from src.config.conf_logs import logger

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.bot.handlers import welcome, books, navigation
from src.bot.handlers.admin import add_book, add_category, add_author
from src.bot.middlewares.middlewares import DbMiddleware

from src.db.database import DataBase
from src.db.migrations.runner import run_migrations

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
db = DataBase()

# Run the bot
async def main() -> None:

    if TOKEN is None:
        logger.error("TOKEN not set")
        return

    dp.include_routers(
        welcome.router,
        books.router,
        navigation.router,
        add_book.router,
        add_category.router,
        add_author.router,
    )

    await run_migrations(db)
    dp.update.middleware(DbMiddleware(db))
    dp.callback_query.middleware(DbMiddleware(db))

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
