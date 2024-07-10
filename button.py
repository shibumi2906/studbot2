from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Простое меню с кнопками
def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Привет")],
            [KeyboardButton(text="Пока")]
        ],
        resize_keyboard=True
    )
    return keyboard

# Кнопки с URL-ссылками
def url_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Новости", url="https://news.example.com")],
            [InlineKeyboardButton(text="Музыка", url="https://music.example.com")],
            [InlineKeyboardButton(text="Видео", url="https://video.example.com")]
        ]
    )
    return keyboard

# Динамическое изменение клавиатуры
def dynamic_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
        ]
    )
    return keyboard

def dynamic_options():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
            [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
        ]
    )
    return keyboard
