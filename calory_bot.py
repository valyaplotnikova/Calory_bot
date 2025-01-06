import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, FSInputFile
from dotenv import load_dotenv

from keyboards import *
from crud_functions import *


load_dotenv()

api = os.getenv('API')

storage = MemoryStorage()
bot = Bot(token=api)

dp = Dispatcher(storage=storage)
initiate_db()
drop_db()
complete_db()

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


@dp.message(F.text.lower().in_('расчитать'))
async def main_menu(message):
    await message.answer(
        text='Выберите опцию:',
        reply_markup=kb
    )


@dp.message(F.text.lower().in_('купить'))
async def get_buying_list(message):
    result = get_all_products()
    try:
        for res in result:
            file_path = f'images/{res[0]}.jpg'
            if os.path.exists(file_path):
                photo = FSInputFile(file_path)
                await message.answer_photo(photo)
                await message.answer(text=f'Название: {res[1]} | Описание: {res[2]} | Цена: {res[-1]}')
            else:
                await message.answer(f'Файл {file_path} не найден.')  # Сообщаем, если файл не найден

        await message.answer(
            text='Выберите продукт:',
            reply_markup=product_kb
        )
    except Exception as e:
        await message.answer(f'Произошла ошибка: {str(e)}')


@dp.callback_query(F.data.lower().in_('product_buying'))
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.callback_query(F.data.lower().in_('formulas'))
async def get_formulas(call):
    await call.message.answer('BMR = 10 * вес + 6.25 * рост - 5 * возраст + 5')
    await call.answer()


@dp.callback_query(F.data.lower().in_('calories'), StateFilter(default_state))
async def set_age(call, state: UserState):
    await call.message.answer('Введите свой возраст:')
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
