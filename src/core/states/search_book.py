from aiogram.fsm.state import State, StatesGroup

class SearchBook(StatesGroup):
    book_name = State()
