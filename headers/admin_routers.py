from os import getenv

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from dotenv import load_dotenv

from fsm import AdminFSM

from database import CRUD

load_dotenv()

admin_router = Router()

lists_admins = list(getenv("admins_list"))
FIRST_ADMIN = str(getenv("FIRST_ADMIN"))

lists_admins.append(FIRST_ADMIN)

@admin_router.message(Command("statistic"))
async def statistic(message: Message):
    if "@" + str(message.from_user.username) in lists_admins:
        await message.answer(f"Текущая статистика:\n\n"
                             f"Всего пользователей: {await CRUD.get_all_users()}\n"
                             f"Всего заказов: {await CRUD.get_all_orders()}\n"
                             f"Положительных отзывов: {await CRUD.get_negative_or_positive_feedback(positive=True)}\n"
                             f"Отрицательных отзывов: {await CRUD.get_negative_or_positive_feedback(positive=False)}\n")
    else:
        await message.answer("Вы не обладаете правами администратора")


@admin_router.message(Command("add_admin"))
async def add_admin(message: Message, state: FSMContext):
    if "@" + str(message.from_user.username) in lists_admins:
        await state.set_state(AdminFSM.add_admin_state)
        await message.answer("Введите username нового администратора")


@admin_router.message(AdminFSM.add_admin_state)
async def add_admin_state(message: Message, state: FSMContext):
    if "@" + str(message.from_user.username) in lists_admins:
        try:
            admin_username = message.text
            lists_admins.append(admin_username)
            await state.clear()
            await message.answer("Администратор добавлен")
        except:
            await message.answer("Некоректный формат записи")


@admin_router.message(Command("remove"))
async def remove_admin(message: Message, state: FSMContext):
    if "@" + str(message.from_user.username) in lists_admins:
        await state.set_state(AdminFSM.remove_admin_state)
        await message.answer("Введите username удаляемого администратора")


@admin_router.message(AdminFSM.remove_admin_state)
async def add_admin_state(message: Message, state: FSMContext):
    if "@" + str(message.from_user.username) in lists_admins:
        try:
            admin_username = message.text
            lists_admins.remove(admin_username)
            await state.clear()
            await message.answer("Администратор удален")
        except:
            await message.answer("Некоректный формат записи или администратор уже удален")


@admin_router.message(Command("all_admins"))
async def remove_admin(message: Message):
    if "@" + str(message.from_user.username) in lists_admins:
        text = f"Все админы:\n\n"
        for index in range(2, len(lists_admins)):
            text += f"{index - 1}: {lists_admins[index]}\n"

        await message.answer(text)
