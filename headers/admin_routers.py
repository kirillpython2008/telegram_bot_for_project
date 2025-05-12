from os import getenv

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from dotenv import load_dotenv

from fsm import AdminFSM

load_dotenv()

admin_router = Router()

lists_admins = list(getenv("admins_list"))
FIRST_ADMIN = str(getenv("FIRST_ADMIN"))

lists_admins.append(FIRST_ADMIN)

@admin_router.message(Command("statistic"))
async def statistic(message: Message):
    if str(message.from_user.id) in lists_admins:
        await message.answer("statistic")
    else:
        await message.answer("Вы не обладаете правами администратора")


@admin_router.message(Command("add_admin"))
async def add_admin(message: Message, state: FSMContext):
    await state.set_state(AdminFSM.add_admin_state)
    await message.answer("Введите id нового администратора")


@admin_router.message(AdminFSM.add_admin_state)
async def add_admin_state(message: Message, state: FSMContext):
    try:
        text = message.text

        lists_admins.append(text)
        await state.clear()
        await message.answer("Администратор добавлен")
    except:
        await message.answer("Некоректный формат записи")
