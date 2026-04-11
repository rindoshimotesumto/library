from typing import Optional
from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from src.data.database import Database
from src.config.logs_conf import logger
from pydantic import BaseModel


class ChannelsType(BaseModel):
    chat_id: int
    title: str
    invite_link: str
    is_active: Optional[bool] = None

class MandatoryChannels:
    def __init__(self, bot: Bot, db: Database):
        self.bot = bot
        self.db = db

    async def is_active(self, chat_id: int) -> bool:
        sql = """
        SELECT 1 FROM mandatory_channels WHERE chat_id = $1
        """
        result = await self.db.fetch_val(sql, chat_id)
        return bool(result)

    async def add_chat(self, chat_id: int) -> bool:
        try:
            chat_info = await self.bot.get_chat(chat_id)
            title = chat_info.title
            invite_link = chat_info.invite_link

            if not invite_link:
                invite_link = await self.bot.export_chat_invite_link(chat_id)

            sql = """
            INSERT INTO mandatory_channels (chat_id, title, invite_link) 
            VALUES ($1, $2, $3)
            ON CONFLICT (chat_id) DO UPDATE 
            SET title = $2, invite_link = $3 
            """

            await self.db.execute(sql, chat_id, title, invite_link)
            return True

        except TelegramAPIError as e:
            logger.error(f"Не удалось получить информацию о чате {chat_id}: {e}")
            return False

        except Exception as e:
            logger.error(f"Ошибка базы данных при добавлении канала {chat_id}: {e}")
            return False

    async def remove_chat(self, chat_id: int) -> bool:
        sql = """
        DELETE FROM mandatory_channels WHERE chat_id = $1
        """

        try:
            await self.db.execute(sql, chat_id)
            return True
        except Exception as e:
            logger.error(f"Ошибка базы данных при удалении канала {chat_id}: {e}")
            return False

    async def get_chat(self, chat_id: int) -> ChannelsType | None:
        sql = "SELECT * FROM mandatory_channels WHERE chat_id = $1"
        result = await self.db.fetch_one(sql, chat_id)

        if not result:
            return None

        return ChannelsType(**dict(result))

    async def get_all_chats(self) -> list[ChannelsType]:
        sql = "SELECT * FROM mandatory_channels WHERE is_active = true"
        result = await self.db.fetch_all(sql)

        if not result:
            return []

        return [ChannelsType(**dict(row)) for row in result]