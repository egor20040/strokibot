from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keybord_products = InlineKeyboardMarkup(row_width=1,
                                         inline_keyboard=[
                                             [
                                                 InlineKeyboardButton(
                                                     text="Строки РФ|Данные паспорта",
                                                     callback_data="string"

                                                 ),
                                             ],
                                             [
                                                 InlineKeyboardButton(
                                                     text="⬅️ Назад",
                                                     callback_data="back_menu"

                                                 ),
                                             ]
                                         ]
                                         )
