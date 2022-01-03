from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Товары"),
            KeyboardButton(text="Профиль"),
        ],
    ],
    resize_keyboard=True
)
