from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.bot.states.add import AddBook
from src.i18n.uz import UZ_TEXTS

from src.db.database import DataBase
from src.db.repo.books import BookRepository, Book
from src.db.repo.categories import CategoriesRepository
from src.db.repo.authors import AuthorRepository

from src.bot.keyboards.inline import categories_keyboard, authors_keyboard

from src.config.conf_logs import logger

router = Router()


# === 1. СТАРТ ===
@router.callback_query(F.data == "admin:b:add")
async def start_add_book(call: CallbackQuery, state: FSMContext, db: DataBase):
    await state.clear()
    category_repo = CategoriesRepository(db)
    categories = await category_repo.get_categories()

    await call.message.edit_text(
        UZ_TEXTS["admin:prompt_book_category"],
        reply_markup= await categories_keyboard(categories)
    )
    await state.set_state(AddBook.category_id)


# === 2. КАТЕГОРИЯ ===
@router.callback_query(AddBook.category_id)
async def book_category(call: CallbackQuery, state: FSMContext, db: DataBase):
    await call.answer()
    await state.update_data(category_id=int(call.data.removeprefix("category:show:")))

    authors_repo = AuthorRepository(db)
    authors = await authors_repo.get_authors()

    await call.message.edit_text(
        UZ_TEXTS["admin:prompt_book_author"],
        reply_markup=await authors_keyboard(authors)
    )

    await state.set_state(AddBook.author_id)


# === 3. АВТОР ===
@router.callback_query(AddBook.author_id)
async def book_author(call: CallbackQuery, state: FSMContext, db: DataBase):
    await call.answer()
    await state.update_data(author_id=int(call.data.removeprefix("author:")))
    await call.message.answer(UZ_TEXTS["admin:prompt_book_cover"])
    await state.set_state(AddBook.cover_file_id)


# === 4. ОБЛОЖКА (Только фото!) ===
@router.message(AddBook.cover_file_id, F.photo)
async def book_cover_file_id(message: Message, state: FSMContext, db: DataBase):
    # Берем самое большое разрешение фото
    file_id = message.photo[-1].file_id
    await state.update_data(cover_file_id=file_id)

    await message.answer(UZ_TEXTS["admin:prompt_book_name"])
    await state.set_state(AddBook.book_name)


# Если вместо фото прислали текст или файл
@router.message(AddBook.cover_file_id)
async def book_cover_invalid(message: Message):
    await message.answer(UZ_TEXTS["admin:err_not_photo"])


# === 5. НАЗВАНИЕ ===
@router.message(AddBook.book_name)
async def book_name(message: Message, state: FSMContext, db: DataBase):
    await state.update_data(book_name=message.text)
    await message.answer(UZ_TEXTS["admin:prompt_book_desc"])
    await state.set_state(AddBook.description)


# === 6. ОПИСАНИЕ ===
@router.message(AddBook.description)
async def book_description(message: Message, state: FSMContext, db: DataBase):
    await state.update_data(description=message.text)
    await message.answer(UZ_TEXTS["admin:prompt_book_year"])
    await state.set_state(AddBook.year_of_publication)


# === 7. ГОД ИЗДАНИЯ ===
@router.message(AddBook.year_of_publication)
async def book_year_of_publication(message: Message, state: FSMContext, db: DataBase):
    if not message.text.isdigit():
        return await message.answer(UZ_TEXTS["admin:err_invalid_number"])

    await state.update_data(year_of_publication=int(message.text))

    # Добавил пропущенный вопрос про вес
    await message.answer(UZ_TEXTS["admin:prompt_book_weight"])
    await state.set_state(AddBook.weight)


# === 8. КОЛ-ВО СТРАНИЦ ===
@router.message(AddBook.weight)
async def book_weight(message: Message, state: FSMContext, db: DataBase):
    if not message.text.isdigit():
        return await message.answer(UZ_TEXTS["admin:err_invalid_number"])

    await state.update_data(weight=int(message.text))
    await message.answer(UZ_TEXTS["admin:prompt_book_file"])
    await state.set_state(AddBook.book_file)


# === 9. ФАЙЛЫ ===
@router.message(AddBook.book_file)
async def book_weight(message: Message, state: FSMContext, db: DataBase):

    if not message.document:
        return

    await state.update_data(book_file_id=message.document.file_id)
    await message.answer(UZ_TEXTS["admin:prompt_book_lang"])
    await state.set_state(AddBook.language)


# === 10. ЯЗЫК (ФИНАЛ: СОХРАНЕНИЕ В БД) ===
@router.message(AddBook.language)
async def book_language(message: Message, state: FSMContext, db: DataBase):
    # 1. Сохраняем последний ответ (язык)
    await state.update_data(language=message.text)

    # 2. Получаем все собранные данные
    data = await state.get_data()

    # 3. Формируем объект датакласса
    new_book = Book(
        category_id=data["category_id"],
        author_id=data["author_id"],
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
        logger.info(f"{book_id} -> {data['book_file_id']}")
        await repo.add_book_file(book_id, data["book_file_id"])
        await message.answer(UZ_TEXTS["admin:msg_book_added"])

    except Exception as e:
        await message.answer(UZ_TEXTS["error:db_error"])
        return