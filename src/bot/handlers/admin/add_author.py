from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.db.database import DataBase
from src.i18n.uz import UZ_TEXTS
from src.bot.states.add import AddAuthor
from src.db.repo.authors import AuthorRepository

router = Router()

@router.callback_query(F.data == "admin:a:add")
async def add_category(call: Message, state: FSMContext, db: DataBase):
    await state.clear()
    await call.message.edit_text(UZ_TEXTS["admin:prompt_author_name"])
    await state.set_state(AddAuthor.author_name)


@router.message(AddAuthor.author_name)
async def prompt_category_name(message: Message, state: FSMContext, db: DataBase):
    author_repo = AuthorRepository(db)

    try:
        await author_repo.add_author(message.text.title())
        await message.answer(UZ_TEXTS["admin:msg_author_added"])

    except Exception as e:
        await message.answer(UZ_TEXTS["error:db_error"])
        return

    finally:
        await state.clear()