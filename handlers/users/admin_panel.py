from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandHelp

from documents.locate import DOC_DIR
from keyboards.inline.admin_keyboard import keyboard_a, keybord_admin
from keyboards.inline.callback_datas import set_string_price, set_mailing
from loader import dp
from utils.db_api import quick_commands as commands


@dp.message_handler(chat_id=417804053, commands=["create_product"])
async def add_item(message: types.Message):
    await commands.create_price()


@dp.message_handler(CommandHelp(), chat_id=-1001657326519)
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/set_price_string - Установвить цену строки',
        '/mailing - Сделайть рассылку',
        '/total_users - количество пользоватлей бота'
    ]
    await message.answer('\n'.join(text))


@dp.message_handler(chat_id=-1001657326519, commands=["total_users"])
async def add_item(message: types.Message):
    users = await commands.select_all_users()
    await message.answer(f"Всего пользователй бота: {len(users)}")


@dp.message_handler(chat_id=-1001657326519, commands=["set_price_string"])
async def add_item(message: types.Message, state: FSMContext):
    await message.answer("Введите цену одной строки:")
    await state.set_state("string_price")


@dp.callback_query_handler(chat_id=-1001657326519, text='cancel_set_price')
async def cancel_price(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer("Отмена установки цены")


@dp.message_handler(chat_id=-1001657326519, state='string_price')
async def string_price(message: types.Message, state: FSMContext):
    price = message.text
    if price.isdigit():
        await message.answer(f"Цена {price} р за 1 строку", reply_markup=keyboard_a(int(price)))
        await state.finish()
    else:
        await message.answer("Введите корректную цену")
        await state.set_state("string_price")


@dp.callback_query_handler(set_string_price.filter(text_name="set_string_price"))
async def accept_price(call: types.CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    await call.message.delete()
    price = callback_data.get("price")
    await commands.update_price_string(int(price))
    await call.message.answer(f"{call.from_user.username} изменил цену строки \n\n"
                              f"Текущая цена за 1 стрноку {price} р")


@dp.message_handler(chat_id=-1001657326519, commands=["mailing"])
async def mailing(message: types.Message, state: FSMContext):
    await message.answer("Ввдите сообщение которое хотите разослать")
    await state.set_state("mailing")


@dp.message_handler(chat_id=-1001657326519, state='mailing')
async def add_milling(message: types.Message, state: FSMContext):
    await state.finish()
    users = await commands.select_all_users()
    i = 0
    for user in users:
        i += 1
        await dp.bot.send_message(chat_id=user.chat_id, text=message.text)
    await message.answer(f"Сообщение отправлено {i} пользователям")


@dp.callback_query_handler(text='mailing', chat_id=-1001657326519)
async def accept_price(call: types.CallbackQuery, state: FSMContext):
    print("Ок")
    await call.answer(cache_time=60)
    data = await state.get_data()
    text = data.get("text")
    print(text)

    users = await commands.select_all_users()
    for user in users:
        await dp.bot.send_message(chat_id=user.chat_id, text=text)


@dp.message_handler(chat_id=-1001657326519, content_types=['document'])
async def scan_message(msg: types.Message):
    document_id = msg.document.file_id
    file_info = await dp.bot.get_file(document_id)
    fi = file_info.file_path
    name = msg.document.file_name
    i = 0
    await dp.bot.download_file(file_path=fi, destination=f"documents/{name}")
    with open(DOC_DIR / name, "r", encoding="UTF8") as file:
        for line in file:
            if len(line) > 10:
                i += 1
                await commands.add_string(line)
    count = await commands.get_count_product()
    await dp.bot.send_message(msg.chat.id, f"В базу данных успешно загружено {i} строк\n\n"
                                           f"Всего строк доступно к покупке {count}")
