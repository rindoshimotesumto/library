from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ContentType
from aiogram.fsm.state import State, StatesGroup

from src.i18n.i18n import t

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


@router.message(AddBook.cover)
async def addbook(message: Message, state: FSMContext, ) -> None:

    if message.content_type != ContentType.PHOTO:
        await message.answer(t("choose:category"))
        return None


    await state.update_data(cover=message.photo[-1].file_id)
    await state.set_state(AddBook.category_id)
    return None