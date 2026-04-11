from typing import Optional
from pydantic import BaseModel, validate_call
from datetime import datetime

from src.data.database import Database
from src.config.logs_conf import logger

from src.i18n.i18n import Langs

class UserDataType(BaseModel):
    id: Optional[int] = None
    tg_id: int
    lang: str = Langs.uz.value
    role: str = 'user'
    created_at: Optional[datetime] = None

class UserRepo:
    def __init__(self, db: Database):
        self.db = db

    @validate_call
    async def search_user(self, tg_id: int) -> bool:
        sql = "SELECT 1 FROM users WHERE tg_id = $1"

        try:
            result = await self.db.fetch_val(sql, tg_id)
            return bool(result)

        except Exception as e:
            logger.exception(f"Ошибка проверки пользователя {tg_id}")
            return False

    @validate_call
    async def get_user(self, tg_id: int) -> UserDataType | None:
        sql = "SELECT * FROM users WHERE tg_id = $1"

        try:
            result = await self.db.fetch_one(sql, tg_id)

            if result is None:
                return None

            return UserDataType(**dict(result))

        except Exception as e:
            logger.exception(f"Ошибка получения данных пользователя {tg_id}")
            return None

    @validate_call
    async def add_user(self, data: UserDataType) -> UserDataType | None:
        sql = """
            INSERT INTO users (tg_id, lang, role) 
            VALUES ($1, $2, $3) 
            ON CONFLICT (tg_id)
            DO UPDATE SET tg_id = EXCLUDED.tg_id 
            RETURNING *
        """

        try:
            result = await self.db.fetch_one(sql, data.tg_id, data.lang, data.role)

            if result is None:
                return None

            return UserDataType(**dict(result))

        except Exception as e:
            logger.exception(f"Ошибка добавления пользователя {data.tg_id}")
            return None

    @validate_call
    async def update_lang(self, tg_id: int, new_lang: Langs) -> None:
        sql = "UPDATE users SET lang = $1 WHERE tg_id = $2"
        params = [new_lang.value, tg_id]

        try:
            await self.db.execute(sql, *params)

        except Exception as e:
            logger.exception(f"Ошибка обновление языка юзреа ID: {tg_id}")