from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from i18n.uz import UZ_TEXTS

from bot.ui.inline_kb import main_menu
from bot.ui.inline_kb import show_book_list

from db.database import DataBase
from db.repo.books import BooksService



router = Router()
db = DataBase()
books_service = BooksService(db)


@router.callback_query(F.data == "back:menu")
async def click_back_to_menu(callback: CallbackQuery):
    await callback.answer()
    keyboard = await main_menu()

    if not isinstance(callback.message, Message):
        return

    await callback.message.edit_text(UZ_TEXTS["start"], reply_markup=keyboard)
