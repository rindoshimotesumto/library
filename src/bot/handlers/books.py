import os
import asyncio
from pyrogram import Client

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.i18n.uz import UZ_TEXTS, LANGS_FORMAT
from src.bot.keyboards.inline import books_keyboard, back_btn, more_btn, InlineKeyboardBuilder, back_task
from src.db.repo.books import BookRepository, Book
from src.db.database import DataBase
from src.db.repo.stats import StatsRepository, Stats, StatsField
from src.db.repo.users import UsersRepository, User
from src.db.repo.authors import AuthorRepository
from src.bot.states.edit import EditBookName
from src.ai.ai_service import get_content

from src.config.conf_logs import logger

from pars_tg_channel import send_audio_to_bot

router = Router()
api_id = os.getenv("MY_ACC_ID")
api_hash = os.getenv("MY_ACC_HASH")
bot_username = "@miniProjectsBot"

@router.callback_query(F.data.startswith("ai:desc:"))
async def get_book_desc(call: CallbackQuery, db: DataBase):
    await call.answer()

    book_id = int(call.data.split(":")[-1])
    book = await BookRepository(db).get_book(book_id)

    # МАГИЯ ЗДЕСЬ: Оборачиваем синхронную функцию в поток, а затем в Task
    task = asyncio.create_task(asyncio.to_thread(get_content, book.book_name, book.author_id))

    step = 0
    icons = ["⏳", "⌛️"]

    # Теперь метод .done() точно есть и всё работает
    while not task.done():
        text = f"{icons[step % 2]} Kitob uchun tavsif yozilmoqda{'.' * (step % 4)}"

        try:
            await call.message.edit_text(text)
        except Exception as e:
            pass  # Игнорим ошибку, если текст не изменился

        step += 1
        await asyncio.sleep(0.7)

    # Выводим результат
    result = await task
    await call.message.edit_text(result or "Ma'lumot topilmadi.", parse_mode="HTML", reply_markup=await back_task(book_id))


@router.callback_query(F.data.startswith("book:show"))
async def show_book(call: CallbackQuery, state: FSMContext, db: DataBase):
    await call.answer()
    stats_repo = StatsRepository(db)
    users_repo = UsersRepository(db)
    books_repo = BookRepository(db)

    user = await users_repo.get_user(call.from_user.id)
    call_btn_text = call.data.removeprefix("book:show:")

    kb = InlineKeyboardBuilder()

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
        kb.adjust(1, 2)
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
        f"<b>Reyting: {book.rating} ⭐️</b>"
        # f"<b><a href='{book.book_file_link}'>Havola 🔗</a></b>"
    )

    stats = await stats_repo.get_stats(user.user_id, book.id)
    await more_btn(kb, book.id, book.category_id, bool(stats.liked))
    await back_btn(kb, "books", book.category_id)
    kb.adjust(1, 2)

    try:
        await call.message.answer_photo(
            photo=book.cover_file_id,
            caption=caption,
            reply_markup=kb.as_markup()
        )

        await call.message.delete()

    except Exception as e:
        await call.message.edit_text(text=caption, reply_markup=kb.as_markup())


@router.callback_query(F.data == "admin:b:edit")
async def edit_book_name(call: CallbackQuery, state: FSMContext, db: DataBase):
    await call.answer()
    await call.message.edit_text("Kitob yangi nomini kiriting...")
    await state.set_state(EditBookName.book_name)


@router.message(EditBookName.book_name)
async def edit_book_name_2(message: Message, state: FSMContext, db: DataBase):
    await state.update_data(book_name=message.text)
    await message.answer(f"Kitob ID -sini kiriting...")

    await state.set_state(EditBookName.book_id)


@router.message(EditBookName.book_id)
async def edit_book_name_3(message: Message, state: FSMContext, db: DataBase):
    if message.text.isdigit() and isinstance(message, Message):
        data = await state.get_data()
        x = await BookRepository(db).update_book_name(int(message.text), data.get("book_name", " "))

        if x:
            await message.answer("✅ O'zgartirildi")
            return

        await message.answer(f"❌ Xatolik chiqdi")
        return

    await message.answer(f"Kitob ID -sini kiriting...")
    return

@router.message(Command("go"))
async def save_file_ids(message: Message, db: DataBase):
    book_repo = BookRepository(db)
    books = await book_repo.get_books()

    async with Client("user_session", api_id, api_hash) as app:
        for book in books:
            book_obj = Book(**book)

            message_id = int(book_obj.book_file_link.split("/")[-1])
            msg = await app.get_messages("Railway_kutubxona", message_id)

            if msg.audio:
                file_id = msg.audio.file_id
            elif msg.voice:
                file_id = msg.voice.file_id
            elif msg.document:
                file_id = msg.document.file_id
            else:
                continue

            await book_repo.add_book_file(book_obj.id, file_id)

    await message.answer("✅ Готово")

@router.callback_query(F.data.startswith("book:download:"))
async def get_file(call: CallbackQuery, state: FSMContext, db: DataBase):
    await call.answer()

    book_repo = BookRepository(db)
    book_id = int(call.data.removeprefix("book:download:"))

    file = await book_repo.get_book_file(book_id)
    file_id = file['file_id']

    try:
        await call.message.answer_document(document=file_id)
    except Exception:
        try:
            await call.message.answer_audio(audio=file_id)
        except Exception:
            await call.message.answer_voice(voice=file_id)

@router.message(Command("get_file"))
async def get_file(message: Message, command: CommandObject, db: DataBase):
    book_repo = BookRepository(db)

    if not command.args:
        await message.answer("Укажи ID книги")
        return

    book_id = int(command.args.strip())
    book = await book_repo.get_book_file(book_id)

    if not book:
        await message.answer("Файл не найден")
        return

    file_id = book["file_id"]

    try:
        await message.answer_document(document=file_id)
    except Exception:
        try:
            await message.answer_audio(audio=file_id)
        except Exception:
            await message.answer_voice(voice=file_id)