from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import set_string_price, set_mailing, set_add_balance, set_user_info


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


def keyboard_add_balance():
    keybord_admin = InlineKeyboardMarkup(row_width=1,
                                         inline_keyboard=[
                                             [
                                                 InlineKeyboardButton(
                                                     text="Подтвердить",
                                                     callback_data="add_balance_user"

                                                 ),
                                             ],
                                             [
                                                 InlineKeyboardButton(
                                                     text="Отмена",
                                                     callback_data="cancel_add_balance"

                                                 ),
                                             ]
                                         ]
                                         )
    return keybord_admin


def keyboard_user_info(user_id):
    keybord_admin = InlineKeyboardMarkup(row_width=2,
                                         inline_keyboard=[
                                             [
                                                 InlineKeyboardButton(
                                                     text="💵 Пополнить баланс",
                                                     callback_data=set_user_info.new(text_name="add_balance",
                                                                                     user_id=user_id)

                                                 ),
                                                 InlineKeyboardButton(
                                                     text="📩 Получить купленые строки",
                                                     callback_data=set_user_info.new(text_name="get_string",
                                                                                     user_id=user_id)

                                                 ),
                                             ],
                                             [
                                                 InlineKeyboardButton(
                                                     text="💬 Отправить сообщение",
                                                     callback_data=set_user_info.new(text_name="send_message",
                                                                                     user_id=user_id)

                                                 ),
                                             ]
                                         ]
                                         )
    return keybord_admin



