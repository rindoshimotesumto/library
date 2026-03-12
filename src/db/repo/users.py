
class UsersRepository:
    def __init__(self, db):
        self.db = db

    async def add_user(self, tg_id: int):
        sql = """
        INSERT INTO users (tg_id) VALUES (?)
        """

        params = (tg_id,)
        await self.db.execute(sql, params)