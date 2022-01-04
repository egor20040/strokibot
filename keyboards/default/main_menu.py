from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="📖 Наличие товаров"),
            KeyboardButton(text="👤 Профиль"),
        ],
        [
            KeyboardButton(text="💬 Обратная связь"),
        ],
    ],
    resize_keyboard=True
)

cancel = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Отмена"),
        ],
    ],
    resize_keyboard=True, one_time_keyboard=True
)
