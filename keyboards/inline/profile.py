from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keybord_add_money = InlineKeyboardMarkup(row_width=1,
                                         inline_keyboard=[
                                             [
                                                 InlineKeyboardButton(
                                                     text="Пополнить",
                                                     callback_data="add_money"

                                                 ),
                                                 InlineKeyboardButton(
                                                     text="Получить купленые строки",
                                                     callback_data="get_lines"

                                                 ),

                                             ],

                                         ]
                                         )
