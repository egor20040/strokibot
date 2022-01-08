import re

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.main_menu import main_menu
from loader import dp
from utils.db_api import quick_commands as commands


@dp.message_handler(CommandStart(deep_link=re.compile("[0-9]+")))
async def bot_start_deeplink(message: types.Message):
    deep_link_args = message.get_args()
    print(deep_link_args)
    user = await commands.select_user(message.from_user.id)
    if user:
        await message.answer("Выберете категорию которая вам нужна ниже:", reply_markup=main_menu)
    else:
        try:
            user = await commands.select_user(int(deep_link_args))
            count = int(user.invited) + 1
            await commands.update_invited(int(deep_link_args), int(count))
        except:
            deep_link_args = 0
        await commands.add_user(id=message.from_user.id, name=message.from_user.full_name, chat_id=message.chat.id,
                                balance=0, invited=0, bonus_string=0, called=int(deep_link_args))
        await message.answer("Выберете категорию которая вам нужна ниже:", reply_markup=main_menu)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    if user:
        await message.answer("Выберете категорию которая вам нужна ниже:", reply_markup=main_menu)
    else:
        await commands.add_user(id=message.from_user.id, name=message.from_user.full_name, chat_id=message.chat.id,
                                balance=0, invited=0, bonus_string=0)
        await message.answer("Выберете категорию которая вам нужна ниже:", reply_markup=main_menu)
