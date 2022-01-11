from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import CHANNEL_ID, NOTSUB_MESSAGE
from documents.locate import DOC_DIR
from keyboards.inline.channel_subscription import subscription_keyboard
from keyboards.inline.products import keybord_products, keybord_products_buy, keybord_products_cancel, \
    keybord_products_balance
from keyboards.default.main_menu import cancel
from loader import dp
from utils.db_api import quick_commands as commands


def check_sub_channel(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False


@dp.callback_query_handler(text="subchanneldone")
async def sub_channel_done(call: types.CallbackQuery):
    await call.message.delete()
    await call.answer(cache_time=60)
    if check_sub_channel(await dp.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=call.from_user.id)):
        await call.message.answer("Спасибо за подписку ☺️, доступ к функционалу бота открыт")
    else:
        await call.message.answer("Не нашел вашу подписку, убедитесь что подписались на канал",
                                  reply_markup=subscription_keyboard)


@dp.message_handler(text="📖 Наличие товаров")
async def show_menu(message: types.Message):
    if check_sub_channel(await dp.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        await message.answer("Выберете товар, который хотите купить:", reply_markup=keybord_products)
    else:
        await message.answer(NOTSUB_MESSAGE, reply_markup=subscription_keyboard)


@dp.message_handler(text="📖 Наличие товаров", state="buy_string")
async def show_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Выберете товар, который хотите купить:", reply_markup=keybord_products)


@dp.message_handler(text="📖 Наличие товаров", state="add_money")
async def show_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Выберете товар, который хотите купить:", reply_markup=keybord_products)


@dp.callback_query_handler(text="back_menu_product", state="buy")
async def show_menu_a(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await state.finish()
    await call.message.delete()
    await call.message.answer("Выберете товар, который хотите купить:", reply_markup=keybord_products)


@dp.callback_query_handler(text="cancel", state="buy_string")
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await state.finish()
    await call.message.delete()
    await call.message.answer("Выберете товар, который хотите купить:", reply_markup=keybord_products)


@dp.callback_query_handler(text="string")
async def back_profile(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    count = await commands.get_count_product()
    string = await commands.get_product_info('string')
    if count == '':
        count = 0
    await call.message.answer_photo(photo='https://ibb.co/Yjb7qb8',
                                    caption=f"➖➖➖➖➖➖➖➖➖➖➖➖\n"
                                            f"📃 Категория: Строки 🇷🇺|Данные паспорта\n"
                                            f"{string.description}\n\n"
                                            f"Доступно к покупке: {count} шт.\n\n"
                                            f"Введите количество для покупки, стоимость {string.price} ₽ шт.\n"
                                            f"➖➖➖➖➖➖➖➖➖➖➖➖",
                                    reply_markup=keybord_products_cancel)
    await state.set_state("buy_string")
    await state.update_data(count=count)
    await state.update_data(price=string.price)


@dp.message_handler(state="buy_string")
async def update_currency(message: types.Message, state: FSMContext):
    number = message.text
    data = await state.get_data()
    count = data.get("count")
    price = data.get("price")
    if number.isdigit():
        summ = price * int(number)
        if int(number) > count:
            await message.answer(f"Маскимальная  сумма для покупки {count}\n\n"
                                 f"Введите корректное количество.", reply_markup=keybord_products_cancel)
            await state.set_state("buy_string")
        elif int(number) < 2:
            await message.answer(f"Минималбная  сумма для покупки 2\n\n"
                                 f"Введите корректное количество.", reply_markup=keybord_products_cancel)
            await state.set_state("buy_string")
        else:
            await message.answer(f"Вы хотите приобрести {number} строк.\n\n"
                                 f"Итоговая сумма: {summ} р.\n\n"
                                 f"Хотите продолжить?", reply_markup=keybord_products_buy)
            await state.set_state("buy")
            await state.update_data(number=int(number))
            await state.update_data(summ=int(summ))
    else:
        await message.answer(f"Введите корректное количество.", reply_markup=keybord_products_cancel)
        await state.set_state("buy_string")


@dp.callback_query_handler(text="buy", state="buy")
async def buy(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    data = await state.get_data()
    number = data.get("number")
    summ = data.get("summ")
    user = await commands.select_user(call.message.chat.id)
    balance = user.balance - summ
    if balance >= 0:
        stroki = await commands.get_product(count=int(number), user_id=call.message.chat.id)
        await commands.update_balance_buy(id=call.message.chat.id, summ=balance)
        for u in stroki:
            await call.message.answer(u.string)

        await dp.bot.send_message(-1001657326519, f"Пользователь @{call.message.chat.username} (id:/{user.id}), купил {number} строк")
        await state.finish()
    else:
        await state.finish()
        balance *= -1
        await call.message.answer(f"Вам не хватает {balance}, пополните ваш баланс",
                                  reply_markup=keybord_products_balance)
