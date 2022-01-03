from aiogram import types
from aiogram.dispatcher import FSMContext

from documents.locate import DOC_DIR
from keyboards.inline.products import keybord_products
from loader import dp
from utils.db_api import quick_commands as commands


@dp.message_handler(text="Товары")
async def show_menu(message: types.Message):
    await message.answer("Выберете товар, который хотите купить:", reply_markup=keybord_products)


@dp.callback_query_handler(text="string")
async def back_profile(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Можно купить: \n\n"
                              "Введите количество для покупки, стоимость 20 руб штука")
    await state.set_state("buy_string")


@dp.message_handler(state="buy_string")
async def update_currency(message: types.Message, state: FSMContext):
    number = message.text
    if number.isdigit():
        summ = int(number) * 20
        user = await commands.select_user(message.chat.id)
        balance = user.balance - summ
        if balance >= 0:
            await commands.update_balance_buy(id=message.chat.id, summ=balance)
            await message.answer(f"Поздравляем с покупкой {number} строк")
            await state.finish()
        else:
            await message.answer(f"Вам не хватает денег, пополните ваш баланс")
    else:
        await message.answer(f"Введите корректное количество.")
        await state.set_state("buy_string")


@dp.message_handler(content_types=['document'])
async def scan_message(msg: types.Message):
    document_id = msg.document.file_id
    file_info = await dp.bot.get_file(document_id)
    fi = file_info.file_path
    name = msg.document.file_name
    await dp.bot.download_file(file_path=fi, destination=f"documents/{name}")
    with open(DOC_DIR / name, "r", encoding="UTF8") as file:
        for line in file:
            if line != '':
                await commands.add_string(line)
