from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

subscription_keyboard = InlineKeyboardMarkup(row_width=1,
                                             inline_keyboard=[
                                                 [
                                                     InlineKeyboardButton(
                                                         text="Подписаться на канал",
                                                         url='https://t.me/+lS3ErzFMPF4xMTFi'

                                                     ),
                                                 ],
                                                 [
                                                     InlineKeyboardButton(
                                                         text="Подписался",
                                                         callback_data="subchanneldone"

                                                     ),
                                                 ]
                                             ]
                                             )
