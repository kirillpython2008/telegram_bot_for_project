from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from mistral import ask_mistral

from keyboards.reply_keyboards import reply_keyboard
from keyboards.inline_keyboards import inline_keyboard

from fsm import UserFSM

from database import CRUD

user_router = Router()

@user_router.message(Command("start"))
async def say_hello(message: Message, state: FSMContext):
    await state.clear()

    user_id = str(message.from_user.id)

    if not(await CRUD.check_user(user_id=user_id)):
        await CRUD.insert_user(user_id=user_id, username=message.from_user.username)
    text = (f"Здравствуйте, {message.from_user.first_name}!\n\n"
                  f"Добро пожаловать в магазин одежды Fashion Hub.\n"
                  f"Здесь вы можете:\n\n"
                  f"✅Посмотреть наш каталог\n"
                  f"✅Задать вопрос нашему консультанту\n"
                  f"✅Оставить отзыв о продукции\n")

    await message.answer(text,
                         reply_markup=reply_keyboard)

#-------------------------------------catalog-------------------------------------------------
@user_router.message(F.text == "Каталог")
async def show_catalog(message: Message, state: FSMContext):
    await state.clear()

    text = "Выберите интересующую вас категорию:"

    await message.answer(text,
                         reply_markup=inline_keyboard)


@user_router.callback_query(F.data == "t-shirt")
async def catalog_t_shirt(callback: CallbackQuery):
    await callback.message.answer("t-shirt")


@user_router.callback_query(F.data == "pants")
async def catalog_pants(callback: CallbackQuery):
    await callback.message.answer("pants")


@user_router.callback_query(F.data == "hats")
async def catalog_hats(callback: CallbackQuery):
    await callback.message.answer("hats")


@user_router.callback_query(F.data == "shoes")
async def catalog_shoes(callback: CallbackQuery):
    await callback.message.answer("shoes")
#-------------------------------------catalog-------------------------------------------------


#-------------------------------------query---------------------------------------------------
@user_router.message(F.text == "Задать вопрос")
async def ask_question(message: Message, state: FSMContext):
    await state.set_state(UserFSM.ai_state)

    await message.answer("Введите текст вопроса")

@user_router.message(UserFSM.ai_state)
async def ask_question_state(message: Message):
    try:
        text = message.text

        prompt = (f"Представь, что ты работаешь консультантом в магазине одежды,"
                  f"старайся отвечать коротко и информативно, если покупатель спрашивает то,"
                  f"что ты не знаешь, попроси его обратится к каталогу, там есть вся необходимая информация."
                  f"Ничего от себя не придумывай!"
                  f"На данный момент на складе имеется:"
                  f"4 футболки (adidas, gucci, puma, nike),"
                  f"4 кепки (kelvin cline, armani, nike, puma),"
                  f"4 пары штанов (nike, puma, tommi helfiger, armani),"
                  f"4 пары ботинок (adidas, nike, new balance, vans)."
                  f"Покупатель задал вопрос:{text}")
        result = await ask_mistral(prompt)

        await message.answer(result)
    except:
        await message.answer("Пожалйста, отправте отзыв в текстовом формате")
#-------------------------------------query---------------------------------------------------


#-------------------------------------feedback------------------------------------------------
@user_router.message(F.text == "Отзыв")
async def feedback(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(UserFSM.feedback_state)
    await message.answer("Введите текст отзыва")

@user_router.message(UserFSM.feedback_state)
async def feedback_state(message: Message, state: FSMContext):
    try:
        text = message.text

        await CRUD.insert_feedback(user_id=str(message.from_user.id), text_feedback=text)
        await state.clear()

        await message.answer("Отзыв отправлен")
    except:
        await message.answer("Пожалуйста, отправте отзыв в текстовом формате")
#-------------------------------------feedback------------------------------------------------
