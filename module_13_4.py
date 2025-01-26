from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = ReplyKeyboardMarkup()
kb.resize_keyboard = True
button1 = KeyboardButton(text = 'Рассчитать')
button2 = KeyboardButton(text = 'Информация')
kb.add(button1)
kb.add(button2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler(text = ['Рассчитать'])
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await  UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    try:
        await state.update_data(age = int(message.text))
        await message.answer('Введите свой рост:')
        await  UserState.growth.set()
    except ValueError as err:
        await message.answer(f'Возраст - это число, а не {message.text} \U0001F621. '
                             f'Нука введите количеcтво полных лет:')
        return

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    try:
        await state.update_data(growth = float(message.text))
        await message.answer('Введите свой вес:')
        await  UserState.weight.set()
    except ValueError as err:
        await message.answer('Рост должен быть числом в см. Введите свой рост:')
        return

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    try:
        await state.update_data(weight = float(message.text))
        data = await state.get_data()
        calories = 10 * data["weight"] + 6.25 * data["growth"] - 5 * data["age"] + 5
        await message.answer(f'Вы можете покушать на: {calories} калорий.')
        await state.finish()
    except ValueError as err:
        await message.answer(f'Вес должен быть числом в кг, а вы что тут пишите - {message.text} \U0001F602 .'
                             f' Введите свой вес:')
        return

@dp.message_handler()
async def all_messages(message):
    await message.answer(f'извините за нескромный вопрос, может вам калории посчитать?\U0001F60A')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)