import os
import re

from aiogram import types
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters import CommandHelp
from aiogram.types import CallbackQuery

from data.config import admins
from documents.locate import DOC_DIR
from keyboards.inline.admin_keyboard import keyboard_a, keybord_admin, keyboard_add_balance, keyboard_user_info
from keyboards.inline.callback_datas import set_string_price, set_mailing, set_add_balance, set_user_info
from loader import dp
import datetime as dt
from utils.db_api import quick_commands as commands


@dp.message_handler(chat_id=417804053, commands=["create_product"])
async def add_item(message: types.Message):
    await commands.create_price()


@dp.message_handler(regexp='[0-9]+', user_id=admins)
async def send_welcome(message: types.Message, regexp):
    user_id = regexp.string
    user_id = user_id.replace('/', "")
    user = await commands.select_user(int(user_id))
    if user:
        buy_string = await commands.get_purchases_count(int(user_id))
        now = dt.datetime.utcnow()
        created_at = user.created_at + dt.timedelta(hours=3)
        moscow_now = now + dt.timedelta(hours=3)
        start = moscow_now.date() - created_at.date()
        text = [
            f'Пользователь: {user.name}',
            f'Id: {user.id}',
            f'Текущий баланс пользователя: {user.balance}.0 RUB',
            f'Дней в боте: {start.days}',
            f'Купил строк: {buy_string}',
            f'Пригласил пользователей: {user.invited}',
            f'Доступно бонусных строк: {user.bonus_string}',
        ]
        await message.answer('\n'.join(text), reply_markup=keyboard_user_info(user_id))
    else:
        await message.answer("Пользователь не найден")


@dp.callback_query_handler(set_user_info.filter(text_name="get_string"))
async def get_string(call: types.CallbackQuery, callback_data: dict):
    user_id = callback_data.get("user_id")
    buy_string = await commands.get_purchases(int(user_id))
    buy_count = await commands.get_purchases_count(int(user_id))
    await call.answer(cache_time=60)
    if buy_count == 0:
        await call.message.answer("Пользователь пока ничего не купил")
    else:
        with open(f"documents/{call.message.chat.id}.txt", "w", encoding="UTF8") as file:
            for string in buy_string:
                updated_at = string.updated_at + dt.timedelta(hours=3)
                date = updated_at.strftime('%H:%M %d.%m.%y')
                file.write(f"{string.string} , куплен - {date}\n")

        f = open(DOC_DIR / f"{call.message.chat.id}.txt", "rb")
        await dp.bot.send_document(chat_id=call.message.chat.id, document=f)
        os.remove(f"documents/{call.message.chat.id}.txt")


@dp.callback_query_handler(set_user_info.filter(text_name="add_balance"))
async def add_balance(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    user_id = callback_data.get("user_id")
    await call.message.answer("Введите сумму которую хотите добавить пользователю")
    await state.set_state("add_balance")
    await state.update_data(user_id=user_id)


@dp.message_handler(user_id=admins, state='add_balance')
async def send_message1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    try:
        if int(message.text) < 0:
            user = await commands.select_user(int(user_id))
            await commands.update_balance(int(user_id), int(message.text))
            await dp.bot.send_message(chat_id=user.chat_id, text=f"Ваш баланс понизили на {message.text}.0 RUB")
            user = await commands.select_user(int(user_id))
            await message.answer(f"Баланс пользователя уменьшен на {message.text}.0 RUB\n\n"
                                 f"Баланс пользователя: {user.balance}.0 RUB")
            await state.finish()
        else:
            user = await commands.select_user(int(user_id))
            await commands.update_balance(int(user_id), int(message.text))
            await dp.bot.send_message(chat_id=user.chat_id, text=f"Вам на счет добавлено {message.text}.0 RUB")
            user = await commands.select_user(int(user_id))
            await message.answer(f"На счет пользователя добавлено {message.text}.0 RUB\n\n"
                                 f"Баланс пользователя: {user.balance}.0 RUB")
            await state.finish()
    except:
        await message.answer(f"Введите корректную сумму.")
        await state.set_state("add_balance")


@dp.callback_query_handler(set_user_info.filter(text_name="send_message"))
async def send_message(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    user_id = callback_data.get("user_id")
    await call.message.answer("Введите сообщение которое хотите отправить пользователю")
    await state.set_state("send_message")
    await state.update_data(user_id=user_id)


@dp.message_handler(user_id=admins, state='send_message')
async def send_message1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    user = await commands.select_user(int(user_id))
    await dp.bot.send_message(chat_id=user.chat_id, text=message.text)
    await message.answer(f"Сообщение отправлено пользователю {user.name}")
    await state.finish()


@dp.message_handler(chat_id=417804053, commands=["add_users_balance"])
async def add_users_balance(message: types.Message, state: FSMContext):
    await message.answer(f"Введите id пользователя которому хотите пополнить баланс")
    await state.set_state("add_users_balance")


@dp.message_handler(chat_id=417804053, state='add_users_balance')
async def add_users_balance_1(message: types.Message, state: FSMContext):
    user = await commands.select_user(int(message.text))
    if user:
        await message.answer("Введите сумму на которую хотите пополнить баланс")
        await state.set_state("add_users_balance_sum")
        await state.update_data(user_id=message.text)
    else:
        await message.answer("Такого пользоватлея не существует")
        await state.finish()


@dp.message_handler(chat_id=417804053, state='add_users_balance_sum')
async def add_users_balance_1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    user = await commands.select_user(int(user_id))
    await message.answer(f"Вы хотите добавить пользователю: {user.name} {message.text}.0 RUB\n"
                         f"Текущий баланс пользователя: {user.balance}.0 RUB",
                         reply_markup=keyboard_add_balance())
    await state.set_state("add_users_balance_finish")
    await state.update_data(user_id=user_id)
    await state.update_data(balance=message.text)


@dp.callback_query_handler(text='cancel_add_balance', chat_id=417804053, state="add_users_balance_finish")
async def add_users_balance_3(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer("Вы отменили операцию")
    await state.finish()


@dp.callback_query_handler(text='add_balance_user', chat_id=417804053, state="add_users_balance_finish")
async def add_users_balance_2(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    data = await state.get_data()
    user_id = data.get("user_id")
    balance = data.get("balance")
    await commands.update_balance(int(user_id), int(balance))
    user = await commands.select_user(int(user_id))
    await call.message.answer(f"Баланс успешно пополнен, баланс пользователя {user.name} {user.balance}.0 RUB")
    await state.finish()


@dp.message_handler(CommandHelp(), chat_id=-1001657326519)
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/set_price_string - Установвить цену строки',
        '/mailing - Сделайть рассылку',
        '/total_users - количество пользоватлей бота',
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
