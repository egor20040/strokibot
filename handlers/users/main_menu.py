from aiogram import types


from keyboards.default.main_menu import main_menu
from loader import dp


@dp.callback_query_handler(text="back_menu")
async def back_profile(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer("Выберете категорию которая вам нужна ниже:", reply_markup=main_menu)
