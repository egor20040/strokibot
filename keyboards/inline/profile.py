from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keybord_add_money = InlineKeyboardMarkup(row_width=1,
                                         inline_keyboard=[
                                             [
                                                 InlineKeyboardButton(
                                                     text="💶 Пополнить баланс",
                                                     callback_data="method"

                                                 ),
                                                 InlineKeyboardButton(
                                                     text="📩 Получить купленые строки",
                                                     callback_data="get_lines"

                                                 ),

                                             ],
                                             [
                                                 InlineKeyboardButton(
                                                     text="🎁 Получить бонусные строки",
                                                     callback_data="get_bonus_lines"

                                                 ),
                                             ]

                                         ]
                                         )

keyboard_method_replenishment = InlineKeyboardMarkup(row_width=1,
                                                     inline_keyboard=[
                                                         [
                                                             InlineKeyboardButton(
                                                                 text="🥝 QIWI",
                                                                 callback_data="add_money"

                                                             ),

                                                         ],

                                                     ]
                                                     )
