from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.main_menu import main_menu
from loader import dp
from utils.db_api import quick_commands as commands


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    if user:
        await message.answer("Выберете категорию которая вам нужна ниже:", reply_markup=main_menu)
    else:
        await commands.add_user(id=message.from_user.id, name=message.from_user.full_name, chat_id=message.chat.id,
                                balance=0)
        await message.answer("Выберете категорию которая вам нужна ниже:", reply_markup=main_menu)

