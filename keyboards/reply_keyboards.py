from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

list_buttons = [[KeyboardButton(text="Каталог"), KeyboardButton(text="Отзыв")],
            [KeyboardButton(text="Задать вопрос"), KeyboardButton(text="Корзина")],
                [KeyboardButton(text="Оформить заказ")]]

reply_keyboard = ReplyKeyboardMarkup(keyboard=list_buttons, resize_keyboard=True)
