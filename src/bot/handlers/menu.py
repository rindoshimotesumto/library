from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.ui.inline_kb import back_to_menu
from db.database import DataBase
from db.repo.books import BooksService
from db.repo.categories import CategoriesService
from i18n.uz import UZ_TEXTS

router = Router()
db = DataBase()
books_service = BooksService(db)
categories_service = CategoriesService(db)


@router.callback_query(F.data.startswith("menu:"))
async def callback_h(callback: CallbackQuery):
    await callback.answer()
    
    books = False
    categories = False

    if not callback.data:
        return

    if not isinstance(callback.message, Message):
        return

    keyboard = await back_to_menu()
    call_data = callback.data.removeprefix("menu:")

    if await books_service.has_books():
        books = True
        
    if await categories_service.has_categories():
        categories = True

    if call_data == "books":
        if books:
            await callback.message.edit_text(UZ_TEXTS["books:list"], reply_markup=keyboard)
            return

        await callback.message.edit_text(UZ_TEXTS["no:books"], reply_markup=keyboard)

    elif call_data == "categories":
        if categories:
            await callback.message.edit_text(UZ_TEXTS["categories"], reply_markup=keyboard)
            return
            
        await callback.message.edit_text(UZ_TEXTS["no:categories"], reply_markup=keyboard)

    elif call_data == "search":
        if books:
            await callback.message.edit_text(UZ_TEXTS["search:prompt"], reply_markup=keyboard)
            return

        await callback.message.edit_text(UZ_TEXTS["no:search"], reply_markup=keyboard)

    elif call_data == "profile":
        await callback.message.edit_text(UZ_TEXTS["no:profile"], reply_markup=keyboard)

    elif call_data == "help":
        await callback.message.edit_text(UZ_TEXTS["help"], reply_markup=keyboard)

    elif call_data == "settings":
        await callback.message.edit_text(UZ_TEXTS["no:settings"], reply_markup=keyboard)
