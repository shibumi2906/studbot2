import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from config import API_TOKEN
from button import main_menu, url_menu, dynamic_menu, dynamic_options

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
async def cmd_start(message: Message, state: FSMContext):
    await message.answer("Выберите опцию:", reply_markup=main_menu())

# Хендлер для кнопок "Привет" и "Пока"
@router.message(lambda message: message.text in ["Привет", "Пока"])
async def process_greetings(message: Message):
    if message.text == "Привет":
        await message.answer(f"Привет, {message.from_user.first_name}!")
    elif message.text == "Пока":
        await message.answer(f"До свидания, {message.from_user.first_name}!")

# Хендлер для команды /links
@router.message(Command("links"))
async def cmd_links(message: Message):
    await message.answer("Выберите ссылку:", reply_markup=url_menu())

# Хендлер для команды /dynamic
@router.message(Command("dynamic"))
async def cmd_dynamic(message: Message):
    await message.answer("Выберите опцию:", reply_markup=dynamic_menu())

# Хендлер для обработки нажатий на инлайн-кнопки
@router.callback_query(lambda c: c.data in ["show_more", "option_1", "option_2"])
async def process_callback(callback_query: CallbackQuery):
    if callback_query.data == "show_more":
        await callback_query.message.edit_reply_markup(reply_markup=dynamic_options())
    elif callback_query.data == "option_1":
        await callback_query.message.answer("Вы выбрали Опция 1")
    elif callback_query.data == "option_2":
        await callback_query.message.answer("Вы выбрали Опция 2")
    await callback_query.answer()

# Хендлер для получения имени
@router.message(StateFilter(Form.name))
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Сколько тебе лет?")

# Хендлер для получения возраста
@router.message(lambda message: not message.text.isdigit(), StateFilter(Form.age))
async def process_age_invalid(message: Message):
    return await message.reply("Возраст должен быть числом. Сколько тебе лет?")

@router.message(lambda message: message.text.isdigit(), StateFilter(Form.age))
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await state.set_state(Form.grade)
    await message.answer("В каком ты классе?")

# Хендлер для получения класса (grade)
@router.message(StateFilter(Form.grade))
async def process_grade(message: Message, state: FSMContext):
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
