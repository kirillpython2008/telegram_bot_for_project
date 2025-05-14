from aiogram.fsm.state import State, StatesGroup


class UserFSM(StatesGroup):
    feedback_state = State()
    ai_state = State()
    order_state = State()
    finally_order_state = State()


class AdminFSM(StatesGroup):
    add_admin_state = State()
    remove_admin_state = State()
