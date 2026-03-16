from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.i18n.uz import UZ_TEXTS, LANGS_FORMAT
from src.bot.keyboards.inline import books_keyboard, back_btn, InlineKeyboardBuilder
from src.db.repo.books import BookRepository
from src.db.database import DataBase

from src.config.conf_logs import logger

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

    try:
        await call.message.edit_text(text=UZ_TEXTS["admin:btn_my_books"], reply_markup=book_kb)

    except Exception as e:
        await call.message.answer(text=UZ_TEXTS["admin:btn_my_books"], reply_markup=book_kb)
        await call.message.delete()

@router.callback_query(F.data.startswith("book:show"))
async def show_book(call: CallbackQuery, state: FSMContext, db: DataBase):
    await call.answer()

    books_repo = BookRepository(db)
    book_id = int(call.data.removeprefix("book:show:"))
    book = await books_repo.get_book(book_id)

    logger.info(f"{book}")

    if book is None:
        await call.message.answer("Kitob topilmadi 😔")
        return

    caption = (
        f"<b>{book.book_name} 📚</b>\n"
        f"<b>👤 Muallif: <i>{book.author_id}</i></b>\n"
        f"<b>🗓 Nashr qilingan yil: {book.year_of_publication}</b>\n\n"
        f"<b>Til: {LANGS_FORMAT[book.language]}  /  </b>"
        f"<b>Reyting: {book.rating} ⭐️  /  </b>"
        f"<b><a href='{book.book_file_link}'>Havola 🔗</a></b>"
    )

    kb = InlineKeyboardBuilder()
    await back_btn(kb, "books", book.category_id)

    try:
        await call.message.answer_photo(
            photo=book.cover_file_id,
            caption=caption,
            reply_markup=kb.as_markup()
        )

    except Exception as e:
        await call.message.edit_text(text=caption, reply_markup = kb.as_markup())
        logger.info(f"{e}")

    await call.message.delete()

