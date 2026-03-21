from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.db.database import DataBase
from src.i18n.uz import UZ_TEXTS
from src.bot.states.add import AddCategory
from src.db.repo.categories import CategoriesRepository
from src.bot.keyboards.inline import main_menu
from src.config.conf_logs import logger
router = Router()

@router.callback_query(F.data == "admin:c:add")
async def add_category(call: CallbackQuery, state: FSMContext, db: DataBase):
    await state.clear()
    await call.message.edit_text(UZ_TEXTS["admin:prompt_category_name"])
    await state.set_state(AddCategory.category_name)


@router.message(AddCategory.category_name)
async def prompt_category_name(message: Message, state: FSMContext, db: DataBase):
    categories_repo = CategoriesRepository(db)

    try:
        await categories_repo.add_category(message.text)
        await message.answer(UZ_TEXTS["admin:msg_category_added"], reply_markup=await main_menu(True))

    except Exception as e:
        logger.warning(e)
        await message.answer(UZ_TEXTS["error:db_error"])
        return

    finally:
        await state.clear()