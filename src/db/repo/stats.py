from dataclasses import dataclass
from enum import Enum
from src.db.database import DataBase

@dataclass
class ReturnInfo:
    user_id: int
    book_id: int

@dataclass
class Stats:
    user_id: int
    book_id: int
    book_category_id: int
    liked: int
    watched: int
    read: int
    listened: int
    listening: int
    i_want_to_listen: int
    downloaded: int

class StatsField(str, Enum):
    LIKED = "liked"
    WATCHED = "watched"
    READ = "read"
    LISTENED = "listened"
    LISTENING = "listening"
    I_WANT_TO_LISTEN = "i_want_to_listen"
    DOWNLOADED = "downloaded"

class StatsRepository:
    def __init__(self, db: DataBase):
        self.db = db
        self.table_name = "user_book_stats"

    async def check_info(self, user_id: int, book_id: int) -> int:
        sql = f"""
        SELECT 1 FROM {self.table_name}
        WHERE user_id = ? AND book_id = ?
        """

        params = (user_id, book_id)

        row = await self.db.fetchone(sql, params)
        return row
    
    async def save_data(self, stats: Stats) -> ReturnInfo:
        sql = f"""
        INSERT INTO {self.table_name} (
            user_id, book_id, book_category_id,
            liked, watched, "read",
            listened, listening, i_want_to_listen, downloaded
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        RETURNING user_id, book_id;
        """

        params = (
            stats.user_id,
            stats.book_id,
            stats.book_category_id,
            stats.liked,
            stats.watched,
            stats.read,
            stats.listened,
            stats.listening,
            stats.i_want_to_listen,
            stats.downloaded
        )

        result = await self.db.fetchone(sql, params)
        return ReturnInfo(**result)

    async def update_data(self, stats: Stats) -> ReturnInfo:
        sql = f"""
        UPDATE {self.table_name} SET
            user_id =?, book_id =?, book_category_id =?,
            liked =?, watched =?, "read" =?,
            listened =?, listening =?, i_want_to_listen =?, downloaded =?
        WHERE user_id =? AND book_id =? RETURNING user_id, book_id;
        """

        params = (
            stats.user_id,
            stats.book_id,
            stats.book_category_id,
            stats.liked,
            stats.watched,
            stats.read,
            stats.listened,
            stats.listening,
            stats.i_want_to_listen,
            stats.downloaded,
            stats.user_id,
            stats.book_id,
        )

        result = await self.db.fetchone(sql, params)
        return ReturnInfo(**result)

    async def get_stats(self, user_id: int, book_id: int) -> Stats:
        sql = """
        SELECT
            user_id,
            book_id,
            book_category_id,
            liked,
            watched,
            "read",
            listened,
            listening,
            i_want_to_listen,
            downloaded
        FROM user_book_stats WHERE user_id = ? AND book_id = ?"""
        params = (user_id, book_id)

        row = await self.db.fetchone(sql, params)
        return Stats(**row) if row else None

    async def apply_action(self, user_id: int, book_id: int, category_id: int, field: StatsField, value: int = 1) -> bool:
        current = await self.get_stats(user_id, book_id)

        if current:
            old_value = getattr(current, field.value)
            if field == StatsField.WATCHED:
                new_value = old_value + value

            else:
                new_value = 0 if old_value == 1 else 1

            setattr(current, str(field.value), new_value)
            return await self.update_data(current) is not None

        stats = Stats(
            user_id=user_id,
            book_id=book_id,
            book_category_id=category_id,
            liked=0,
            watched=0,
            read=0,
            listened=0,
            listening=0,
            i_want_to_listen=0,
            downloaded=0,
        )

        setattr(stats, field.value, value)
        return await self.save_data(stats) is not None