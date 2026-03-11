from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.ui.inline_kb import back_to_book_list
from db.database import DataBase
from db.repo.books import BooksService
from db.repo.categories import CategoriesService
from i18n.uz import UZ_TEXTS

router = Router()
db = DataBase()
books_service = BooksService(db)
categories_service = CategoriesService(db)


@router.callback_query(F.data.startswith("book:"))
async def book_handler(callback: CallbackQuery):

    await callback.answer()

    if not callback.data:
        return

    if not isinstance(callback.message, Message):
        return

    call_data = callback.data.removeprefix("book:")

    if call_data.startswith("id:"):
        book_id = int(call_data.removeprefix("id:"))
        book_info = await books_service.get_book(book_id)
        keyboard = await back_to_book_list(book_info["id"])

        text = (
            f"{UZ_TEXTS['book:title']}: <b>{book_info['book_name']}</b>\n"
            f"{UZ_TEXTS['book:author']}: <b>{book_info['author_name']}</b>\n"
            f"{UZ_TEXTS['book:category']}: <b>{book_info['category_name']}</b>\n\n"
            f"{UZ_TEXTS['book:description']}: <i>{book_info['description']}</i>"
        )

        await callback.message.answer_photo(photo=book_info["cover_file_id"], caption=text, reply_markup=keyboard, parse_mode="html")
        await callback.message.delete()

    elif call_data.startswith("download:"):
        book_id = int(call_data.removeprefix("download:"))
        book_file_id = await books_service.get_book_file(book_id)
        await callback.message.answer_document(document=book_file_id["book_file_id"])

