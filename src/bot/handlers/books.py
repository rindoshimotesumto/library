import os
import asyncio
from pyrogram import Client

from aiogram import Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery, MessageOriginChannel, MessageOriginChat
from aiogram.fsm.context import FSMContext

from bot.handlers.welcome import admin
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

async def background_forwarding(books, db: DataBase):
    async with Client("user_session", api_id, api_hash) as app:
        for book in books:
            book_obj = Book(**book)
            try:
                message_id = int(book_obj.book_file_link.split("/")[-1])

                # Вместо forward используем send_cached_media или copy_message
                # Это отправит файл боту, и мы принудительно запишем ID книги в описание
                await app.copy_message(
                    chat_id=bot_username,
                    from_chat_id="Railway_kutubxona",
                    message_id=message_id,
                    caption=f"book_id:{book_obj.id}"  # Пишем ID прямо в описание файла!
                )

                await asyncio.sleep(1.5)
            except Exception as e:
                print(f"Ошибка с книгой {book_obj.id}: {e}")

@router.message(Command("go"))
async def save_file_ids(message: Message, db: DataBase):
    if message.from_user.id not in admin:
        return

    book_repo = BookRepository(db)
    books = await book_repo.get_books()

    # Запускаем пересылку в фоне, не блокируя бота
    asyncio.create_task(background_forwarding(books, db))

    # Сразу отвечаем пользователю, чтобы Telegram закрыл update
    await message.answer("✅ Процесс обновления запущен. Файлы пересылаются боту в фоновом режиме...")


@router.message(F.caption.startswith("book_id:"))
async def handle_forwarded_book(message: Message, db: DataBase):
    book_repo = BookRepository(db)

    # 1. Извлекаем ID книги из подписи
    try:
        book_id = int(message.caption.split(":")[-1])
    except (ValueError, IndexError):
        return

    # 2. Вытаскиваем file_id
    file_id = None
    if message.document:
        file_id = message.document.file_id
    elif message.audio:
        file_id = message.audio.file_id

    if file_id:
        # 3. Просто сохраняем, поиск по ссылке больше не нужен!
        await book_repo.add_book_file(book_id, file_id)
        print(f"✅ Сохранено напрямую: Book ID {book_id} -> File {file_id}")


@router.callback_query(F.data.startswith("book:download:"))
async def get_file(call: CallbackQuery, db: DataBase):
    await call.answer()
    book_repo = BookRepository(db)
    book_id = int(call.data.removeprefix("book:download:"))

    file_data = await book_repo.get_book_file(book_id)
    if not file_data:
        return await call.message.answer("Файл еще не обработан системой.")

    file_id = file_data['file_id']

    # Теперь это сработает без ошибок
    try:
        await call.message.answer_document(document=file_id)
    except Exception:
        try:
            await call.message.answer_audio(audio=file_id)
        except Exception:
            await call.message.answer("Не удалось отправить файл.")


# @router.message(Command("get_file"))
# async def get_file(message: Message, command: CommandObject, db: DataBase):
#     book_repo = BookRepository(db)
#
#     if not command.args:
#         await message.answer("Укажи ID книги")
#         return
#
#     book_id = int(command.args.strip())
#     book = await book_repo.get_book_file(book_id)
#
#     if not book:
#         await message.answer("Файл не найден")
#         return
#
#     file_id = book["file_id"]
#
#     try:
#         await message.answer_document(document=file_id)
#     except Exception:
#         try:
#             await message.answer_audio(audio=file_id)
#         except Exception:
#             await message.answer_voice(voice=file_id)