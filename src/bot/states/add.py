from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ContentType
from aiogram.fsm.state import State, StatesGroup

from datetime import datetime
from urllib.parse import urlparse

from src.i18n.i18n import t
from src.config.logs_conf import logger

router = Router()

class AddBook(StatesGroup):
    cover = State()

    category_id = State()
    collection_id = State()

    title = State()
    author_id = State()

    description = State()
    language = State()

    year_of_publication = State()
    number_of_pages = State()
    weight = State()

    next_part_id = State()
    link = State()

async def validate_link(link: str) -> bool:
    result = urlparse(link)

    try:
        if result.scheme not in ('http', 'https'):
            return False

        if not result.netloc:
            return False

        if "." not in parsed.netloc:
            return False

        return True

    except Exception as e:
        logger.exception()
        return False

@router.message(AddBook.cover)
async def add_book_cover(message: Message, state: FSMContext) -> None:

    cover = ""

    if message.content_type == ContentType.PHOTO:
        cover = message.photo[-1].file_id

    await message.answer(t("choose:category"))
    await state.update_data(cover=cover)

    await state.set_state(AddBook.category_id)
    return

@router.callback_query(AddBook.category_id)
async def add_book_category(query: CallbackQuery, state: FSMContext) -> None:

    if query.data.startswith("c:"):
        c_id = int(query.data.removeprefix("c:"))
        await state.update_data(category_id=c_id)

        await query.message.answer(t("add:collection"))
        await state.set_state(AddBook.collection_id)

    return

@router.callback_query(AddBook.collection_id)
async def add_book_collection(query: CallbackQuery, state: FSMContext) -> None:

    if query.data.startswith("coll:"):
        coll_id = int(query.data.removeprefix("coll:"))
        await state.update_data(collection_id=coll_id)

        await query.message.answer(t("add:title"))
        await state.set_state(AddBook.title)

    return

@router.message(AddBook.title)
async def add_book_title(message: Message, state: FSMContext) -> None:

    if message.content_type == ContentType.TEXT:
        await state.update_data(title=message.text)
        await state.set_state(AddBook.author_id)

    else:
        await message.answer(t("title:invalid"))

    return

@router.callback_query(AddBook.author_id)
async def add_book_author(query: CallbackQuery, state: FSMContext) -> None:

    if query.data.startswith("a:"):
        a_id = int(query.data.removeprefix("a:"))
        await state.update_data(author_id=a_id)

        await query.message.answer(t("add:description"))
        await state.set_state(AddBook.description)

    return

@router.message(AddBook.description)
async def add_book_description(message: Message, state: FSMContext) -> None:

    if message.content_type == ContentType.TEXT:
        await state.update_data(description=message.text)
        await state.set_state(AddBook.language)

        await message.answer(t("add:language"))
        await state.set_state(AddBook.language)

@router.callback_query(AddBook.language)
async def add_book_language(query: CallbackQuery, state: FSMContext) -> None:

    if query.data.startswith("lang:"):
        lang = query.data.removeprefix("lang:")
        await state.update_data(language=lang)

        await query.message.answer(t("add:year_of_publication"))
        await state.set_state(AddBook.year_of_publication)

    return

@router.message(AddBook.year_of_publication)
async def add_book_year_of_publication(message: Message, state: FSMContext) -> None:

    if message.content_type == ContentType.TEXT:
        if message.text.isdigit():
            input_year = int(message.text)
            current_year = datetime.now().year

            if 0 < input_year <= current_year:
                await state.update_data(year_of_publication=input_year)
                await query.message.answer(t("add:number_of_pages"))

                await state.set_state(AddBook.number_of_pages)
                return

    await message.answer(t("year_of_publication:invalid"))
    return

@router.message(AddBook.number_of_pages)
async def add_book_number_of_pages(message: Message, state: FSMContext) -> None:

    if message.content_type == ContentType.TEXT:
        if message.text.isdigit():
            await state.update_data(number_of_pages=int(message.text))
            await message.answer(t("add:link"))

            return

    await message.answer(t("number_of_pages:invalid"))
    return

@router.message(AddBook.link)
async def add_book_link(message: Message, state: FSMContext) -> None:

    if message.content_type == ContentType.TEXT:
        if await validate_link(message.text):
            await state.update_data(link=message.text)
            await state.clear()

    return