from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.ui.inline_kb import back_to_book_list
from db.database import DataBase
from db.repo.books import BooksService
from db.repo.categories import CategoriesService
from i18n.uz import UZ_TEXTS

from config.logging import logger

router = Router()

router = Router()
db = DataBase()
books_service = BooksService(db)
categories_service = CategoriesService(db)


@router.callback_query(F.data == "")
async def show_categorys(callback: CallbackQuery):
    await callback.answer()
    
    