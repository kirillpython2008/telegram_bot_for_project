from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

list_buttons = [[InlineKeyboardButton(text="Верхняя одежда", callback_data="t-shirt"), InlineKeyboardButton(text="Штаны", callback_data="pants")],
                [InlineKeyboardButton(text="Головные уборы", callback_data="hats"), InlineKeyboardButton(text="Обувь", callback_data="shoes")]]

inline_keyboard = InlineKeyboardMarkup(inline_keyboard=list_buttons)
