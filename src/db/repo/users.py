from db.database import DataBase

class UsersService():
    def __init__(self, db: DataBase) -> None:
        self.db = db

    async def get_role(self, tg_id: int) -> dict:
        sql = """
        SELECT
            users.role
        FROM users
        WHERE users.tg_id = ?
        """

        params = (tg_id,)
        row = await self.db.fetchone(sql, params)
        return row