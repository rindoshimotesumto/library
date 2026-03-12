from aiogram.fsm.state import StatesGroup, State

class PaginationState(StatesGroup):
    browse = State()