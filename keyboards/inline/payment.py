from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import set_byi_sell, set_paid


def paid_keyboard(url):
    paid_keyboard = InlineKeyboardMarkup(row_width=2,
                                         inline_keyboard=[
                                             [
                                                 InlineKeyboardButton(
                                                     text="Перейти к оплате по ссылке",
                                                     url=url

                                                 ),

                                             ],
                                             [
                                                 InlineKeyboardButton(
                                                     text="✅ Проверить пополнение ✅",
                                                     callback_data=set_paid.new(text_name="paid")

                                                 ),

                                             ],
                                             [
                                                 InlineKeyboardButton(
                                                     text="❌ Отменить пополнение ❌",
                                                     callback_data="back_profile"

                                                 ),

                                             ]

                                         ]
                                         )
    return paid_keyboard
