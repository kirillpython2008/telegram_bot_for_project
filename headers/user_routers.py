from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from mistral import ask_mistral

from keyboards.reply_keyboards import reply_keyboard
from keyboards.inline_keyboards import (inline_keyboard, create_gender_button,
                                        create_bucket_button, cline_bucket_keyboard, corrected_address_keyboard)

from fsm import UserFSM

from database import CRUD

from address import check_address

user_router = Router()

BUCKET_ALL_ITEMS = ["t-shirt_man_bucket", "pants_man_bucket", "hats_man_bucket", "shoes_man_bucket",
                    "t-shirt_woman_bucket", "pants_woman_bucket", "hats_woman_bucket", "shoes_woman_bucket"]
MAN_ITEMS = ["t-shirt_man", "pants_man", "hats_man", "shoes_man"]
WOMAN_ITEMS = ["t-shirt_woman", "pants_woman", "hats_woman", "shoes_woman"]

DICT_OF_BUCKET_ALL_ITEMS = {
    "t-shirt_man_bucket": "Футболка Adidas мужская\n\n700 руб",
    "t-shirt_woman_bucket": "Футболка Adidas женская\n\n700 руб",

    "pants_man_bucket": "Штаны Nike мужские\n\n1000 руб",
    "pants_woman_bucket": "Штаны Nike женские\n\n1000 руб",

    "hats_man_bucket": "Кепка Puma мужская\n\n500 руб",
    "hats_woman_bucket": "Кепка Puma женская\n\n500 руб",

    "shoes_man_bucket": "Кроссовки New Balance мужские\n\n2000 руб",
    "shoes_woman_bucket": "Кроссовки New Balance женские\n\n2000 руб",

    "t-shirt_man": "Футболка Adidas мужская\n\n700 руб",
    "t-shirt_woman": "Футболка Adidas женская\n\n700 руб",

    "pants_man": "Штаны Nike мужские\n\n1000 руб",
    "pants_woman": "Штаны Nike женские\n\n1000 руб",

    "hats_man": "Кепка Puma мужская\n\n500 руб",
    "hats_woman": "Кепка Puma женская\n\n500 руб",

    "shoes_man": "Кроссовки New Balance мужские\n\n2000 руб",
    "shoes_woman":"Кроссовки New Balance женские\n\n2000 руб",
}


URL_PHOTO = {
    "t-shirt_man": "https://cdn1.ozone.ru/s3/multimedia-m/6008738446.jpg",
    "pants_man": "https://avatars.mds.yandex.net/get-mpic/5346941/img_id8180805022433495503.jpeg/orig",
    "hats_man": "https://avatars.mds.yandex.net/i?id=5b5d31ff877124e52af997686198a1ed5cfced45-10310233-images-thumbs&n=13",
    "shoes_man": "https://avatars.mds.yandex.net/i?id=e6824fb97a219298eec4cadf322ef6a0_l-5103223-images-thumbs&n=13",
    "t-shirt_woman": "https://cdn1.ozone.ru/s3/multimedia-1-n/7077047987.jpg",
    "pants_woman": "https://img.joomcdn.net/dcaac2b8cb51823b7bc729aca0c9ef94d00264e6_original.jpeg",
    "hats_woman": "https://avatars.mds.yandex.net/i?id=ef9fadeec4769e31340f6c7a201b1118_l-5235458-images-thumbs&n=13",
    "shoes_woman": "https://images-eu.ssl-images-amazon.com/images/I/41QaU9u2sqL._UL1000_.jpg"
}


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
    keyboard = await create_gender_button("t-shirt")

    await callback.message.answer("Мужская или женская",
                                  reply_markup=keyboard)


@user_router.callback_query(F.data == "pants")
async def catalog_pants(callback: CallbackQuery):
    keyboard = await create_gender_button("pants")

    await callback.message.answer("Мужская или женская",
                                  reply_markup=keyboard)


@user_router.callback_query(F.data == "hats")
async def catalog_hats(callback: CallbackQuery):
    keyboard = await create_gender_button("hats")

    await callback.message.answer("Мужская или женская",
                                  reply_markup=keyboard)


@user_router.callback_query(F.data == "shoes")
async def catalog_shoes(callback: CallbackQuery):
    keyboard = await create_gender_button("shoes")

    await callback.message.answer("Мужская или женская",
                                  reply_markup=keyboard)


@user_router.callback_query(lambda callback: callback.data in MAN_ITEMS)
async def category_man(callback: CallbackQuery):
    keyboard = await create_bucket_button(callback.data)

    await callback.message.answer_photo(photo=URL_PHOTO[callback.data],
                                        caption=DICT_OF_BUCKET_ALL_ITEMS[callback.data],
                                        reply_markup=keyboard)


@user_router.callback_query(lambda callback: callback.data in WOMAN_ITEMS)
async def category_woman(callback: CallbackQuery):
    keyboard = await create_bucket_button(callback.data)

    await callback.message.answer_photo(photo=URL_PHOTO[callback.data],
                                        caption=DICT_OF_BUCKET_ALL_ITEMS[callback.data],
                                        reply_markup=keyboard)


@user_router.callback_query(lambda callback: callback.data in BUCKET_ALL_ITEMS)
async def bucket_all(callback: CallbackQuery):
    await CRUD.insert_bucket(str(callback.from_user.id), callback.data)
    await callback.answer("Товар добавлен в корзину", show_alert=True)

#-------------------------------------catalog-------------------------------------------------


#-------------------------------------bucket--------------------------------------------------
@user_router.message(F.text == "Корзина")
async def bucket(message: Message):
    try:
        items = await CRUD.read_user_items(str(message.from_user.id))
        list_of_items = items.split("|")

        text = f"На данный момент в вашей корзине есть:\n\n"

        for index in range(1, len(list_of_items)):
            text = text + f"📦 {DICT_OF_BUCKET_ALL_ITEMS[list_of_items[index]]}\n\n"

        await message.answer(text,
                             reply_markup=cline_bucket_keyboard)
    except:
        await message.answer("Ваша корзина пуста")


@user_router.callback_query(F.data == "clean_bucket")
async def clean_bucket(callback: CallbackQuery):
    await CRUD.delete_items(str(callback.from_user.id))

    await callback.answer("Корзина очищена", show_alert=True)
#-------------------------------------bucket--------------------------------------------------


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
                  f"2 футболки (adidas),"
                  f"2 кепки (puma),"
                  f"2 пары штанов (nike),"
                  f"2 пары ботинок (new balance)."
                  f"Покупатель задал вопрос:{text}")
        result = await ask_mistral(prompt)

        await message.answer(result)
    except:
        await message.answer("Пожалйста, отправте отзыв в текстовом формате")
#-------------------------------------query---------------------------------------------------


#-------------------------------------order---------------------------------------------------
@user_router.message(F.text == "Оформить заказ")
async def order(message: Message, state: FSMContext):
    await state.set_state(UserFSM.order_state)

    try:
        items = await CRUD.read_user_items(str(message.from_user.id))
        items.split("|")
        await message.answer("Введите город, улицу и номер дома для доставки")
    except:
        await message.answer("Оформить заказ невозможно, ваша корзина пуста")


@user_router.message(UserFSM.order_state)
async def order_state(message: Message, state: FSMContext):
    user_address = message.text
    result = check_address(user_address)

    if result[1]:
        await message.answer(f"Доставка оформлена на адрес:\n\n"
                             f"🌆 город: {result[0]['city']}\n"
                             f"🛣️ улица: {result[0]['street']}\n"
                             f"🏠 дом: {result[0]['house']}\n\n"
                             f"Адрес верный ?",
                             reply_markup=corrected_address_keyboard)
        await state.clear()
    else:
        await message.answer(result[0])

@user_router.callback_query(F.data == "address_corrected")
async def correct_address(callback: CallbackQuery):
    user_id = str(callback.from_user.id)

    await CRUD.delete_items(user_id=user_id)
    await CRUD.add_order(user_id=user_id)
    await callback.message.answer("Заказ оформлен, ожидайте обратной связи")

@user_router.callback_query(F.data == "address_uncorrected")
async def uncorrected_address(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserFSM.finally_order_state)
    await callback.message.answer("Напишите корректный адрес: Город, улица, дом")

@user_router.message(UserFSM.finally_order_state)
async def order_state(message: Message, state: FSMContext):
    user_address = message.text
    result = check_address(user_address)

    if result[1]:
        await message.answer(f"Доставка оформлена на адрес:\n\n"
                             f"🌆 город: {result[0]['city']}\n"
                             f"🛣️ улица: {result[0]['street']}\n"
                             f"🏠 дом: {result[0]['house']}\n\n"
                             f"Адрес верный ?",
                             reply_markup=corrected_address_keyboard)
        await state.clear()
    else:
        await message.answer(result[0])

#-------------------------------------order---------------------------------------------------


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
