from aiogram.fsm.state import StatesGroup, State

class EditBookName(StatesGroup):
    book_id = State()
    book_name = State()