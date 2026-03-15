from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.i18n.uz import UZ_TEXTS
from src.bot.keyboards.inline import main_menu
from src.db.repo.books import BookRepository
from src.db.database import DataBase

router = Router()

@router.callback_query(F.data.in_(("menu:main", "menu:admin")))
async def back_to_menu(callback: CallbackQuery, state:FSMContext, db: DataBase):
    await callback.answer()

    if callback.data == "menu:main":
        await callback.message.edit_text(UZ_TEXTS["common:start"], reply_markup=await main_menu(False))

    elif callback.data == "menu:admin":
        await callback.message.edit_text(UZ_TEXTS["common:start"], reply_markup=await main_menu(True))