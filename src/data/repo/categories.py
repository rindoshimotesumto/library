from enum import Enum
from typing import Optional

import asyncpg
from datetime import datetime
from pydantic import BaseModel, validate_call

from src.data.database import Database
from src.config.logs_conf import logger

class CategoriesType(BaseModel):
    id: Optional[int] = None
    name: str
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Category:
    def __init__(self, db: Database):
        self.db = db

    @validate_call
    async def get_categories(
        self,
        is_active: bool = True,
        prev_category_id: int = None,
        next_category_id: int = None,
    ) -> list[CategoriesType]:

        sql = "SELECT * FROM categories WHERE is_active = $1"
        args = [is_active]

        if isinstance(prev_category_id, int):
            sql += f" AND id < $2 ORDER BY id DESC LIMIT $2"

        elif isinstance(next_category_id, int):
            sql += f" AND id > $2 ORDER BY id ASC LIMIT $2"

        else:
            sql += f" ORDER BY id DESC LIMIT $2"

        records = await self.db.fetch_all(sql, *args)

        if isinstance(prev_category_id, int):
            records.reverse()

        return [CategoriesType(**dict(record)) for record in records]