from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keybord_products = InlineKeyboardMarkup(row_width=1,
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(
                                                    text="Строки 🇷🇺|Данные паспорта",
                                                    callback_data="string"

                                                ),
                                            ],

                                        ]
                                        )

keybord_products_buy = InlineKeyboardMarkup(row_width=1,
                                            inline_keyboard=[
                                                [
                                                    InlineKeyboardButton(
                                                        text="Купить",
                                                        callback_data="buy"

                                                    ),
                                                ],
                                                [
                                                    InlineKeyboardButton(
                                                        text="⬅️ Назад",
                                                        callback_data="back_menu_product"

                                                    ),
                                                ]
                                            ]
                                            )

keybord_products_cancel = InlineKeyboardMarkup(row_width=1,
                                               inline_keyboard=[
                                                   [
                                                       InlineKeyboardButton(
                                                           text="Отмена",
                                                           callback_data="cancel"

                                                       ),
                                                   ]
                                               ]
                                               )

keybord_products_balance = InlineKeyboardMarkup(row_width=1,
                                               inline_keyboard=[
                                                   [
                                                       InlineKeyboardButton(
                                                           text="Пополнить",
                                                           callback_data="add_money"

                                                       ),
                                                   ]
                                               ]
                                               )
