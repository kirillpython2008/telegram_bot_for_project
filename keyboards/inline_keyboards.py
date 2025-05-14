from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

category_buttons = [[InlineKeyboardButton(text="Верхняя одежда", callback_data="t-shirt"), InlineKeyboardButton(text="Штаны", callback_data="pants")],
                    [InlineKeyboardButton(text="Головные уборы", callback_data="hats"), InlineKeyboardButton(text="Обувь", callback_data="shoes")]]

inline_keyboard = InlineKeyboardMarkup(inline_keyboard=category_buttons)


async def create_gender_button(category: str):
    gender_buttons = [[InlineKeyboardButton(text="Мужская", callback_data=f"{category}_man"),
                               InlineKeyboardButton(text="Женская", callback_data=f"{category}_woman")]]

    gender_keyboard = InlineKeyboardMarkup(inline_keyboard=gender_buttons)

    return gender_keyboard


async def create_bucket_button(item: str):
    bucket_buttons = [[InlineKeyboardButton(text="Добавить в корзину", callback_data=f"{item}_bucket")]]
    bucket_keyboard = InlineKeyboardMarkup(inline_keyboard=bucket_buttons)

    return bucket_keyboard


cline_bucket_buttons = [[InlineKeyboardButton(text="Очистить корзину", callback_data="clean_bucket")]]

cline_bucket_keyboard = InlineKeyboardMarkup(inline_keyboard=cline_bucket_buttons)

corrected_address_buttons = [[InlineKeyboardButton(text="Да", callback_data="address_corrected"),
                              InlineKeyboardButton(text="Нет", callback_data="address_uncorrected")]]

corrected_address_keyboard = InlineKeyboardMarkup(inline_keyboard=corrected_address_buttons)
