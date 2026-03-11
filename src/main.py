import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from bot.handlers import welcome, navigation, menu, book, admin, search
from config.logging import logger

from db.database import DataBase
from db.migrations.runner import run_migrations

load_dotenv(dotenv_path="./bot/.env")
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
db = DataBase()

# Run the bot
async def main() -> None:

    if TOKEN is None:
        logger.error("⚠️ TOKEN is invalid.")
        return

    dp.include_routers(
        welcome.router,
        navigation.router,
        menu.router,
        book.router,
        search.router,
        admin.router,
    )

    bot = Bot(token=TOKEN)

    await run_migrations(db)

    logger.info("🚀 BOT STARTED")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
