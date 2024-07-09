import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from config import API_TOKEN

# Инициализация бота
bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
storage = MemoryStorage()
dp = Dispatcher()
router = Router()

# Состояния
class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

# Хендлер для команды /start
@router.message(Command("start"))
async def cmd_start(message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Привет! Как тебя зовут?")

# Хендлер для получения имени
@router.message(StateFilter(Form.name))
async def process_name(message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Сколько тебе лет?")

# Хендлер для получения возраста
@router.message(lambda message: not message.text.isdigit(), StateFilter(Form.age))
async def process_age_invalid(message):
    return await message.reply("Возраст должен быть числом. Сколько тебе лет?")

@router.message(lambda message: message.text.isdigit(), StateFilter(Form.age))
async def process_age(message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await state.set_state(Form.grade)
    await message.answer("В каком ты классе?")

# Хендлер для получения класса (grade)
@router.message(StateFilter(Form.grade))
async def process_grade(message, state: FSMContext):
    await state.update_data(grade=message.text)
    data = await state.get_data()

    # Сохраняем данные в базу данных
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (name, age, grade)
        VALUES (?, ?, ?)
    ''', (data['name'], data['age'], data['grade']))
    conn.commit()
    conn.close()

    await message.answer("Спасибо! Твои данные сохранены.")
    await state.clear()

# Добавляем роутер к диспетчеру
dp.include_router(router)

async def main():
    await dp.start_polling(bot, storage=storage)

if __name__ == '__main__':
    asyncio.run(main())
