from aiogram import Router, F
from aiogram.types import CallbackQuery

from src.bot.services.cache_service import DefaultUserData
from src.i18n.i18n import t
from src.bot.keyboards.inline import menu_kb

router = Router()

@router.callback_query(F.data == "check:subscribe")
async def check_sub(call: CallbackQuery, user: DefaultUserData):
    await call.answer()
    await call.message.delete()