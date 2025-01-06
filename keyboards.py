from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


button_1 = KeyboardButton(text='Расчитать')
button_2 = KeyboardButton(text='Информация')

my_keyboard = ReplyKeyboardMarkup(
    keyboard=[[button_1, button_2,]],
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
