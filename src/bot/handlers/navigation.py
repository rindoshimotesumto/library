import os
from dotenv import load_dotenv

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.i18n.uz import UZ_TEXTS
from src.bot.keyboards.inline import main_menu
from src.db.database import DataBase
from src.config.conf_logs import logger
from src.bot.handlers.welcome import check_user

router = Router()
load_dotenv()
channel_id = os.getenv("CHANNEL_ID")

@router.callback_query(F.data.in_(("menu:main", "menu:admin")))
async def back_to_menu(callback: CallbackQuery, state:FSMContext, db: DataBase):
    await callback.answer()

    if callback.data == "menu:main":
        await callback.message.edit_text(UZ_TEXTS["common:start"], reply_markup=await main_menu(False))

    elif callback.data == "menu:admin":
        await callback.message.edit_text(UZ_TEXTS["common:start"], reply_markup=await main_menu(True))


@router.callback_query(F.data == "check_sub")
async def check_subscription_callback(callback: CallbackQuery, state: FSMContext, db: DataBase, bot: Bot):
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=callback.from_user.id)

        if member.status in ["member", "administrator", "creator"]:
            admin_menu = False

            if await check_user(callback, db) == "admin":
                admin_menu = True

            await callback.message.edit_text(UZ_TEXTS["common:start"], reply_markup=await main_menu(admin_menu))

        elif member.status == "kicked":
            await callback.answer(
                text=UZ_TEXTS["sub:kicked"],
                show_alert=True
            )
        else:
            await callback.answer(
                text=UZ_TEXTS["sub:not_found"],
                show_alert=True
            )

    except Exception as e:
        logger.warning(f"{e}")
        await callback.answer(UZ_TEXTS["error:db_error"])
