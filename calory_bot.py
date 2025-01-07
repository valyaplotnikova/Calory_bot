import os

from aiogram import Bot, Dispatcher, F, types
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
    """
    Состояния для пользователя, связанные с вводом данных о здоровье.
    """
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    """
    Состояния для регистрации пользователя.
    """
    username = State()
    email = State()
    age = State()


@dp.message(CommandStart(), StateFilter(default_state))
async def start(message: Message):
    """
    Обрабатывает команду "/start".
    Отправляет приветственное сообщение и предлагает начать взаимодействие с ботом.

    :param message: Объект сообщения от пользователя.
    """
    await message.answer(text='Привет!\nЯ бот помогающий твоему здоровью.'
                         '\n Введите "Calories" для расчета Вашей нормы потребления калорий',
                         reply_markup=my_keyboard
                         )


@dp.message(F.text.lower().in_('расчитать'))
async def main_menu(message):
    """
    Обрабатывает сообщение с текстом 'расчитать'.
    Отправляет меню с опциями для пользователя.

    :param message: Объект сообщения от пользователя.
    """
    await message.answer(
        text='Выберите опцию:',
        reply_markup=kb
    )


@dp.message(F.text.lower().in_('купить'))
async def get_buying_list(message):
    """
    Обрабатывает сообщение с текстом 'купить'.
    Отправляет список доступных продуктов с изображениями и описанием.

    :param message: Объект сообщения от пользователя.
    """
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
    """
    Обрабатывает нажатие на кнопку 'product_buying'.
    Отправляет сообщение о успешной покупке продукта.

    :param call: Объект обратного вызова от пользователя.
    """
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message(F.text.lower().in_('регистрация'), StateFilter(default_state))
async def sing_up(message: types.Message, state: RegistrationState):
    """
    Обрабатывает сообщение с текстом 'регистрация'.
    Запрашивает имя пользователя для регистрации.

    :param message: Объект сообщения от пользователя.
    :param state: Текущее состояние регистрации.
    """
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await state.set_state(RegistrationState.username)


@dp.message(StateFilter(RegistrationState.username))
async def set_username(message: types.Message, state: RegistrationState.username):
    """
    Обрабатывает ввод имени пользователя.
    Проверяет существование пользователя в базе данных и запрашивает email, если имя уникально.

    :param message: Объект сообщения от пользователя.
    :param state: Текущее состояние для ввода имени пользователя.
    """
    username = message.text

    # Проверка существования пользователя в базе данных
    if is_included(username):
        await message.answer("Пользователь существует, введите другое имя:")
    else:
        await state.update_data(username=username)
        await message.answer("Введите свой email:")
        await state.set_state(RegistrationState.email)


@dp.message(StateFilter(RegistrationState.email))
async def set_email(message: types.Message, state: RegistrationState.email):
    """
    Обрабатывает ввод email.
    Запрашивает возраст пользователя после успешного ввода email.

    :param message: Объект сообщения от пользователя.
    :param state: Текущее состояние для ввода email.
    """
    email = message.text
    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await state.set_state(RegistrationState.age)


@dp.message(StateFilter(RegistrationState.age))
async def set_age(message: types.Message, state: RegistrationState.age):
    """
    Обрабатывает ввод возраста.
    Завершает процесс регистрации и сохраняет данные пользователя в базе данных.

    :param message: Объект сообщения от пользователя.
    :param state: Текущее состояние для ввода возраста.
    """
    age = message.text
    data = await state.get_data()

    username = data.get('username')
    email = data.get('email')

    # Добавление пользователя в базу данных
    add_user(username, email, age)

    await message.answer("Регистрация прошла успешно!")
    await state.clear()


@dp.callback_query(F.data.lower().in_('formulas'))
async def get_formulas(call):
    """
    Обрабатывает нажатие на кнопку 'formulas'.
    Отправляет формулу для расчета BMR (Basal Metabolic Rate).

    :param call: Объект обратного вызова от пользователя.
    """
    await call.message.answer('BMR = 10 * вес + 6.25 * рост - 5 * возраст + 5')
    await call.answer()


@dp.callback_query(F.data.lower().in_('calories'), StateFilter(default_state))
async def set_age(call, state: UserState):
    """
    Обрабатывает нажатие на кнопку 'calories'.
    Запрашивает возраст для расчета нормы калорий.

    :param call: Объект обратного вызова от пользователя.
    :param state: Текущее состояние для ввода возраста.
    """
    await call.message.answer('Введите свой возраст:')
    await state.set_state(UserState.age)


@dp.message(StateFilter(UserState.age))
async def set_growth(message: Message, state: UserState.age):
    """
    Обрабатывает ввод возраста.
    Запрашивает рост после успешного ввода возраста.

    :param message: Объект сообщения от пользователя.
    :param state: Текущее состояние для ввода возраста.
    """
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await state.set_state(UserState.growth)


@dp.message(StateFilter(UserState.growth))
async def set_growth(message: Message, state: UserState.growth):
    """
    Обрабатывает ввод роста.
    Запрашивает вес после успешного ввода роста.

    :param message: Объект сообщения от пользователя.
    :param state: Текущее состояние для ввода роста.
    """
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await state.set_state(UserState.weight)


@dp.message(StateFilter(UserState.weight))
async def send_calories(message: Message, state: UserState.weight):
    """
    Обрабатывает ввод веса.
    Рассчитывает и отправляет норму калорий на основе введенных данных.

    :param message: Объект сообщения от пользователя.
    :param state: Текущее состояние для ввода веса.
    """
    await state.update_data(weight=message.text)
    data = await state.get_data()

    # Извлекаем данные
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])

    # Формула Миффлина - Сан Жеора (для женщин)
    # BMR = 10 * вес + 6.25 * рост - 5 * возраст + 5
    calories = 10 * weight + 6.25 * growth - 5 * age + 5

    await message.answer(f"Ваша норма калорий: {calories:.2f} ккал.")
    await state.clear()


@dp.message()
async def all_massages(message: Message):
    """
    Обрабатывает любые текстовые сообщения, кроме команд "/start".
    Напоминает пользователю о команде "/start" для начала общения.

    :param message: Объект сообщения от пользователя.
    """
    await message.answer('Введите команду /start, чтобы начать общение')


if __name__ == '__main__':
    dp.run_polling(bot)
