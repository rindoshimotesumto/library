from dataclasses import dataclass


@dataclass(slots=True)
class Users:
    tg_id: int
    username: str
    first_name: str
    last_name: str
    role: str
    language: str