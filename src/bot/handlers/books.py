from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.i18n.uz import UZ_TEXTS, LANGS_FORMAT
from src.bot.keyboards.inline import books_keyboard, back_btn, more_btn, InlineKeyboardBuilder
from src.db.repo.books import BookRepository
from src.db.database import DataBase
from src.db.repo.stats import StatsRepository, Stats, StatsField
from src.db.repo.users import UsersRepository, User

from src.config.conf_logs import logger

router = Router()

# @router.callback_query(F.data == "menu:books")
# async def book_menu(call: CallbackQuery, state: FSMContext, db: DataBase):
#     await call.answer()
#
#     books_repo = BookRepository(db)
#     book_list = await books_repo.get_books()
#     books_count =await books_repo.get_books_page_count()
#
#     if not book_list:
#         await call.message.edit_text(text=UZ_TEXTS["error:not_found"])
#         return
#
#     book_kb = await books_keyboard(book_list, books_count)
#
#     try:
#         await call.message.edit_text(text=UZ_TEXTS["admin:btn_my_books"], reply_markup=book_kb)
#
#     except Exception as e:
#         await call.message.answer(text=UZ_TEXTS["admin:btn_my_books"], reply_markup=book_kb)
#         await call.message.delete()

@router.callback_query(F.data.startswith("book:show"))
async def show_book(call: CallbackQuery, state: FSMContext, db: DataBase):
    await call.answer()
    stats_repo = StatsRepository(db)
    users_repo = UsersRepository(db)
    books_repo = BookRepository(db)

    user = await users_repo.get_user(call.from_user.id)
    call_btn_text = call.data.removeprefix("book:show:")

    kb = InlineKeyboardBuilder()
    kb.adjust(2)

    if call_btn_text.startswith(("like:", "liked:")):
        if call_btn_text.startswith("like:"):
            like_ = 1
            txt = "like:"

        else:
            like_ = 0
            txt = "liked:"

        data = call_btn_text.removeprefix(txt).split(":")
        c_id = int(data[0])
        b_id = int(data[-1])
        await stats_repo.apply_action(user.user_id, b_id, c_id, StatsField.LIKED, like_)

        await more_btn(kb, b_id, c_id, bool(like_))
        await back_btn(kb, "books", c_id)
        await call.message.edit_reply_markup(reply_markup=kb.as_markup())
        return

    book_id = int(call_btn_text)
    book = await books_repo.get_book(book_id)

    if user:
        await stats_repo.apply_action(user.user_id, book_id, book.category_id, StatsField.WATCHED, 1)
    else:
        logger.warning(f"User: {user}")

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

    stats = await stats_repo.get_stats(user.user_id, book.id)
    await more_btn(kb, book.id, book.category_id, bool(stats.liked))
    await back_btn(kb, "books", book.category_id)

    try:
        await call.message.answer_photo(
            photo=book.cover_file_id,
            caption=caption,
            reply_markup=kb.as_markup()
        )

        await call.message.delete()

    except Exception as e:
        await call.message.edit_text(text=caption, reply_markup=kb.as_markup())