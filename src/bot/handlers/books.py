from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.i18n.uz import UZ_TEXTS
from src.bot.keyboards.inline import books_keyboard
from src.db.repo.books import BookRepository
from src.db.database import DataBase

router = Router()

@router.callback_query(F.data == "menu:books")
async def book_menu(call: CallbackQuery, state: FSMContext, db: DataBase):
    await call.answer()

    books_repo = BookRepository(db)
    book_list = await books_repo.get_books()

    if not book_list:
        await call.message.edit_text(text=UZ_TEXTS["error:not_found"])
        return

    book_kb = await books_keyboard(book_list)
    await call.message.edit_text(text=UZ_TEXTS["admin:btn_my_books"], reply_markup=book_kb)


@router.callback_query(F.data.startswith("book:show"))
async def show_book(call: CallbackQuery, state: FSMContext, db: DataBase):
    await call.answer()

    books_repo = BookRepository(db)
    book_id = int(call.data.removeprefix("book:show:"))
    book = await books_repo.get_book(book_id)

    if book is None:
        await call.message.answer("Kitob topilmadi 😔")
        return

    caption = (
        f"📚 <b>{book.book_name}</b>\n"
        f"📅 <b>Nashr qilingan yili:</b> {book.year_of_publication}\n\n"
        f"📝 <b>Tavsif:</b> <i>{book.description}</i>\n\n"
        # f"⚖️ <b>Вес:</b> {book.weight}\n"
        f"🌐 <b>Til:</b> {book.language}\n"
        f"⭐️ <b>Reyting:</b> {book.rating}/5.0"
    )

    try:
        await call.message.answer_photo(
            photo=book.cover_file_id,
            caption=caption
        )

    except Exception as e:
        await call.message.edit_text(text=caption)

    await call.message.delete()

