from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


button_1 = KeyboardButton(text='Расчитать')
button_2 = KeyboardButton(text='Информация')
button_3 = KeyboardButton(text='Купить')

my_keyboard = ReplyKeyboardMarkup(
    keyboard=[[button_1, button_2],
              [button_3]],
    resize_keyboard=True,
    one_time_keyboard=True
)

inline_button_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_button_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')

kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [inline_button_1, inline_button_2]
    ],
    resize_keyboard=True,
)


product_button_1 = InlineKeyboardButton(text='Ежедневник1', callback_data='product_buying')
product_button_2 = InlineKeyboardButton(text='Ежедневник2', callback_data='product_buying')
product_button_3 = InlineKeyboardButton(text='Ежедневник3', callback_data='product_buying')
product_button_4 = InlineKeyboardButton(text='Ежедневник4', callback_data='product_buying')

product_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [product_button_1, product_button_2, product_button_3, product_button_4]
    ],
    resize_keyboard=True,
)
