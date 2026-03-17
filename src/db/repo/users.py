from aiogram.types import User
from dataclasses import dataclass
from src.db.database import DataBase


@dataclass
class User:
    user_id: int
    tg_id: int
    role: str
    lang: str

class UsersRepository:
    def __init__(self, db: DataBase):
        self.db = db

    async def add_user(self, tg_id: int, role: str = "user", lang: str = "uz") -> None:
        sql = """
        INSERT INTO users (tg_id, role, lang) VALUES (?, ?, ?)
        """

        params = (tg_id, role, lang)
        await self.db.execute(sql, params)

    async def get_user(self, tg_id: int) -> User:
        sql = """
        SELECT 
            id AS user_id,
            tg_id,
            role,
            lang
        FROM users WHERE users.tg_id = ?
        """

        params = (tg_id, )
        row = await self.db.fetchone(sql, params)
        return User(**row) if row else None