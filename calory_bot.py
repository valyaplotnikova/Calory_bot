from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

api = '7115803232:AAF67W6cAht1Gh_od5sg-CTN9un2ZABDqJ4'

storage = MemoryStorage()
bot = Bot(token=api)

dp = Dispatcher(storage=storage)

button_1 = KeyboardButton(text='Расчитать')
button_2 = KeyboardButton(text='Информация')

my_keyboard = ReplyKeyboardMarkup(
    keyboard=[[button_1, button_2,]],
    resize_keyboard=True,
    one_time_keyboard=True
)


# Класс состояний
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart(), StateFilter(default_state))
async def start(message: Message):
    await message.answer(text='Привет!\nЯ бот помогающий твоему здоровью.'
                         '\n Введите "Calories" для расчета Вашей нормы потребления калорий',
                         reply_markup=my_keyboard
                         )


@dp.message(F.text.lower().in_('расчитать'), StateFilter(default_state))
async def set_age(message: Message, state: UserState):
    await message.answer('Введите свой возраст:')
    await state.set_state(UserState.age)  # Устанавливаем состояние age


@dp.message(StateFilter(UserState.age))
async def set_growth(message: Message, state: UserState.age):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await state.set_state(UserState.growth)  # Устанавливаем состояние growth


@dp.message(StateFilter(UserState.growth))
async def set_growth(message: Message, state: UserState.growth):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await state.set_state(UserState.weight)  # Устанавливаем состояние weight


@dp.message(StateFilter(UserState.weight))
async def send_calories(message: Message, state: UserState.weight):
    await state.update_data(weight=message.text)
    data = await state.get_data()  # Получаем все данные

    # Извлекаем данные
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    # Формула Миффлина - Сан Жеора (для женщин)
    # BMR = 10 * вес + 6.25 * рост - 5 * возраст + 5
    calories = 10 * weight + 6.25 * growth - 5 * age + 5

    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал.")
    await state.clear()  # Завершаем состояние


# Этот хэндлер будет срабатывать на любые текстовые сообщения,
# кроме команд "/start"
@dp.message()
async def all_massages(message: Message):
    await message.answer('Введите команду /start, чтобы начать общение')


if __name__ == '__main__':
    dp.run_polling(bot)
