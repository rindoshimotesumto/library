import os
from dotenv import load_dotenv

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from typing import Callable, Dict, Any

from src.bot.keyboards.inline import get_sub_keyboard, ChanellInfo
from src.config.conf_logs import logger
from src.i18n.uz import UZ_TEXTS

load_dotenv(".env")
channel_id = os.getenv("CHANNEL_ID")
channel_data = {}

class DbMiddleware(BaseMiddleware):
    def __init__(self, db):
        self.db = db

    async def __call__(
        self,
        handler: Callable,
        event,
        data: Dict[str, Any]
    ):
        data["db"] = self.db
        return await handler(event, data)


class CheckSubscriberMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable,
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ):
        user_id = event.from_user.id

        if isinstance(event, CallbackQuery) and event.data == "check_sub":
            return await handler(event, data)

        try:
            if channel_data.get(channel_id, None) is None:
                channel_info = await event.bot.get_chat(chat_id=channel_id)
                channel_name = channel_info.title

                if channel_info.username:
                    channel_link = f"https://t.me/{channel_info.username}"

                elif channel_info.invite_link:
                    channel_link = channel_info.invite_link

                else:
                    link_obj = await event.bot.create_chat_invite_link(chat_id=channel_id)
                    channel_link = link_obj.invite_link

                channel_data[channel_id] = [channel_id, channel_link, channel_name]

            logger.info(f"data: {channel_data}")
            await event.bot.send_message(
                chat_id=user_id,
                text=UZ_TEXTS["sub:required"],
                reply_markup=await get_sub_keyboard([ChanellInfo(*channel_data[channel_id])]),
            )
            return

        except Exception as e:
            logger.info(f"{e} / {channel_id}")
            return await handler(event, data)