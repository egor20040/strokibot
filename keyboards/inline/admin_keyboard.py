from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import set_string_price, set_mailing


def keyboard_a(price):
    keybord_admin = InlineKeyboardMarkup(row_width=1,
                                         inline_keyboard=[
                                             [
                                                 InlineKeyboardButton(
                                                     text="Подтвердить",
                                                     callback_data=set_string_price.new(text_name="set_string_price",
                                                                                        price=price)

                                                 ),
                                             ],
                                             [
                                                 InlineKeyboardButton(
                                                     text="Отмена",
                                                     callback_data="cancel_set_price"

                                                 ),
                                             ]
                                         ]
                                         )
    return keybord_admin


keybord_admin = InlineKeyboardMarkup(row_width=1,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(
                                                 text="Отпрпвить всем пользователям",
                                                 callback_data="mailing"

                                             ),
                                         ],
                                         [
                                             InlineKeyboardButton(
                                                 text="Отмена",
                                                 callback_data="back_menu"

                                             ),
                                         ]
                                     ]
                                     )
