from aiogram.utils.callback_data import CallbackData

set_byi_sell = CallbackData("set", "text_name", "summ")
set_paid = CallbackData("set", "text_name")
set_string_price = CallbackData("set", "text_name", "price")
set_mailing = CallbackData("set", "text_name", "text")
set_add_balance = CallbackData("set", "text_name", "user_id", "balance")
set_user_info = CallbackData("set", "text_name", "user_id")
