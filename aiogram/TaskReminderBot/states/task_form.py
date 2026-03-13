from aiogram.fsm.state import StatesGroup, State


class TaskForm(StatesGroup):
    """States for the task creation form."""
    waiting_for_text = State()
    waiting_for_time = State()