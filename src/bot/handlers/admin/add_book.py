import asyncio
import time
import re

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from src.bot.states.add import AddBook, AddAuthor, AddCategory
from src.i18n.uz import UZ_TEXTS

from src.db.database import DataBase
from src.db.repo.books import BookRepository, Book
from src.db.repo.categories import CategoriesRepository
from src.db.repo.authors import AuthorRepository

from src.bot.keyboards.inline import categories_keyboard, authors_keyboard, main_menu
from src.bot.keyboards.reply import next_state
from src.config.conf_logs import logger

router = Router()
TG_INTERNAL_LINK = r'https?://t\.me/c/\d+/\d+(?:/\d+)?'

@router.callback_query(F.data == "admin:b:add")
async def start_add_book(call: CallbackQuery, state: FSMContext, db: DataBase):
    await state.clear()
    category_repo = CategoriesRepository(db)
    categories = await category_repo.get_categories()

    if len(categories) == 0:
        await state.clear()
        await call.message.edit_text(UZ_TEXTS["admin:prompt_category_name"])
        await state.set_state(AddCategory.category_name)
        return

    await call.message.edit_text(
        UZ_TEXTS["admin:prompt_book_category"],
        reply_markup= await categories_keyboard(categories, to="admin"))

    await state.set_state(AddBook.category_id)

@router.callback_query(AddBook.category_id)
async def book_category(call: CallbackQuery, state: FSMContext, db: DataBase):
    await call.answer()
    await state.update_data(category_id=int(call.data.removeprefix("category:show:")))

    authors_repo = AuthorRepository(db)
    authors = await authors_repo.get_authors()

    if len(authors) == 0:
        await state.clear()
        await call.message.edit_text(UZ_TEXTS["admin:btn_add_author"])
        await state.set_state(AddAuthor.author_name)
        return

    await call.message.edit_text(
        UZ_TEXTS["admin:prompt_book_author"],
        reply_markup=await authors_keyboard(authors))

    await state.set_state(AddBook.author_id)

@router.callback_query(AddBook.author_id)
async def book_author(call: CallbackQuery, state: FSMContext, db: DataBase):
    await call.answer()
    await state.update_data(author_id=int(call.data.removeprefix("author:")))
    await call.message.edit_text(UZ_TEXTS["admin:prompt_book_cover"])
    await state.set_state(AddBook.cover_file_id)

@router.message(AddBook.cover_file_id, F.photo)
async def book_cover_file_id(message: Message, state: FSMContext, db: DataBase):
    file_id = message.photo[-1].file_id
    await state.update_data(cover_file_id=file_id)

    await message.answer(UZ_TEXTS["admin:prompt_book_name"])
    await state.set_state(AddBook.book_name)

@router.message(AddBook.cover_file_id)
async def book_cover_invalid(message: Message):
    await message.answer(UZ_TEXTS["admin:err_not_photo"])

@router.message(AddBook.book_name)
async def book_name(message: Message, state: FSMContext, db: DataBase):
    await state.update_data(book_name=message.text)
    await message.answer(UZ_TEXTS["admin:prompt_book_year"])
    await state.set_state(AddBook.year_of_publication)

@router.message(AddBook.description)
async def book_description(message: Message, state: FSMContext, db: DataBase):
    await state.update_data(description=message.text)
    await message.answer(UZ_TEXTS["admin:prompt_book_year"])
    await state.set_state(AddBook.year_of_publication)

@router.message(AddBook.year_of_publication)
async def book_year_of_publication(message: Message, state: FSMContext, db: DataBase):

    await state.update_data(description="-")

    if not message.text.isdigit():
        return await message.answer(UZ_TEXTS["admin:err_invalid_number"])

    await state.update_data(year_of_publication=int(message.text))

    await message.answer(UZ_TEXTS["admin:prompt_book_file"], reply_markup=await next_state())
    await state.set_state(AddBook.book_files_list)

@router.message(AddBook.weight)
async def book_weight(message: Message, state: FSMContext, db: DataBase):
    if not message.text.isdigit():
        return await message.answer(UZ_TEXTS["admin:err_invalid_number"])

    await state.update_data(weight=int(message.text))
    await message.answer(UZ_TEXTS["admin:prompt_book_file"], reply_markup=await next_state())
    await state.set_state(AddBook.book_files_list)

@router.message(AddBook.book_files_list)
async def book_files(message: Message, state: FSMContext):
    await state.update_data(weight=1)

    if message.text == "Keyingisi ➡️":
        data = await state.get_data()
        file_list = data.get("book_files_list", [])

        if not file_list:
            await state.update_data(book_files_list="None")

        await message.answer(UZ_TEXTS['admin:prompt_book_link'], reply_markup=ReplyKeyboardRemove())
        await state.set_state(AddBook.book_file_link)
        return

    file_id = None
    if message.document:
        file_id = message.document.file_id
    elif message.photo:
        file_id = message.photo[-1].file_id
    elif message.voice:
        file_id = message.voice.file_id
    elif message.audio:
        file_id = message.audio.file_id

    if not file_id:
        return  # Если это не файл и не кнопка, игнорируем

    data = await state.get_data()

    file_list = data.get("book_files_list", [])
    if not isinstance(file_list, list):
        file_list = []

    file_list.append(file_id)

    current_time = time.time()
    await state.update_data(book_files_list=file_list, last_upload_time=current_time)

    await asyncio.sleep(1.5)

    new_data = await state.get_data()
    if new_data.get("last_upload_time") != current_time:
        return

    total_files = len(new_data.get("book_files_list", []))
    await message.answer(f"{UZ_TEXTS['admin:prompt_book_link']} ({total_files} ✅)",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(AddBook.book_file_link)


@router.message(AddBook.book_file_link, F.text)
async def process_tg_link(message: Message, state: FSMContext, db: DataBase):
    match = re.search(TG_INTERNAL_LINK, message.text)

    if not match:
        await message.answer(
            "❌ Havola formati noto'g'ri.\n"
            "Topicdagi fayl havolasini yuboring\n"
            "Masalan: https://t.me/c/123456/789"
        )
        return

    book_link = match.group(0)

    await state.update_data(
        book_file_link=book_link,
        language="uz")

    data = await state.get_data()

    new_book = Book(
        category_id=data["category_id"],
        author_id=data["author_id"],
        book_file_link=data["book_file_link"],
        cover_file_id=data["cover_file_id"],
        book_name=data["book_name"],
        description=data["description"],
        year_of_publication=data["year_of_publication"],
        weight=data["weight"],
        language=data["language"],
        rating=0.0  # По умолчанию при создании
    )

    await state.clear()

    repo = BookRepository(db)
    try:
        book_id = await repo.add_book(new_book)

        if not isinstance(data["book_files_list"], str):
            for book_file in data["book_files_list"]:
                await repo.add_book_file(book_id, book_file)

        await message.answer(UZ_TEXTS["admin:msg_book_added"], reply_markup=await main_menu(True))

    except Exception as e:
        logger.warning(f"[{message.from_user.username}] / {e}")
        await message.answer(UZ_TEXTS["error:db_error"], reply_markup=await main_menu(True))
        return