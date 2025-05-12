from aiogram.fsm.state import State, StatesGroup


class UserFSM(StatesGroup):
    feedback_state = State()
    ai_state = State()


class AdminFSM(StatesGroup):
    add_admin_state = State()
