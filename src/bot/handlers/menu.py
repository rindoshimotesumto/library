from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.ui.inline_kb import back_to_menu, show_book_list
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

    categories = 0
    books = 0

    if not callback.data:
        return

    if not isinstance(callback.message, Message):
        return

    keyboard = await back_to_menu()
    call_data = callback.data.removeprefix("menu:")

    if call_data == "books":
        book_list = await books_service.get_books()

        if book_list:
            books_kb = await show_book_list(book_list)
            await callback.message.answer(UZ_TEXTS["books:list"], reply_markup=books_kb)
            await callback.message.delete()
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
