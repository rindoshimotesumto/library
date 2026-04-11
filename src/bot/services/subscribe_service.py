import os
from typing import Optional

from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from dotenv import load_dotenv

from src.config.logs_conf import logger
from src.data.database import Database
from src.data.repo.mandatory_channels import MandatoryChannels, ChannelsType

load_dotenv()

class SubscribeService:
    def __init__(self, bot: Bot, db: Database):
        self.bot = bot
        self.db = db

    async def check_subscribe_status(self, user_id: int) -> tuple[list[ChannelsType], bool]:
        chats = await MandatoryChannels(self.bot, self.db).get_all_chats()

        if chats:
            for chat in chats:
                try:
                    chat_id = chat.chat_id
                    chat_member = await self.bot.get_chat_member(chat_id=chat_id, user_id=user_id)

                    if chat_member.status in [
                        ChatMemberStatus.LEFT, ChatMemberStatus.KICKED, ChatMemberStatus.RESTRICTED
                    ]:
                        return chats, False

                except Exception as e:
                    logger.exception(f"Ошибка при попытке получить информацию о юзере по ID: {user_id}")
                    return chats, False

        return chats, True