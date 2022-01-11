import os

from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink, hcode, hbold
import logging

from data import config
from data.config import admins, CHANNEL_ID, NOTSUB_MESSAGE
from documents.locate import DOC_DIR
from handlers.users.products import check_sub_channel
from keyboards.default.main_menu import main_menu
from aiogram.dispatcher import FSMContext
import datetime as dt

from keyboards.inline.callback_datas import set_paid
from keyboards.inline.channel_subscription import subscription_keyboard
from keyboards.inline.payment import paid_keyboard
from keyboards.inline.profile import keybord_add_money, keyboard_method_replenishment
from utils.db_api import quick_commands as commands
from loader import dp
from utils.misc.qiwi import Payment, NoPaymentFound, NotEnoughMoney


@dp.message_handler(text="👤 Профиль")
async def show_menu(message: types.Message):
    if check_sub_channel(await dp.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        user = await commands.select_user(message.from_user.id)
        buy_string = await commands.get_purchases_count(message.chat.id)
        bot_user = await dp.bot.get_me()
        await message.answer(f"🔑 ID: {message.from_user.id}\n"
                             f"💰 Ваш баланс: {user.balance}.0 RUB\n\n"
                             f"💸 Вы купили строк: {buy_string}\n"
                             f"🎁 Бонусные строки: {user.bonus_string}\n"
                             f"🗣 Пригласили пользователей: {user.invited}\n\n"
                             f"🤝 Ваша реферальная ссылка: http://t.me/{bot_user.username}?start={message.chat.id}",
                             reply_markup=keybord_add_money, disable_web_page_preview=True)
    else:
        await message.answer(NOTSUB_MESSAGE, reply_markup=subscription_keyboard)


@dp.message_handler(text="👤 Профиль", state="buy_string")
async def show_menu(message: types.Message, state: FSMContext):
    await state.finish()
    user = await commands.select_user(message.from_user.id)
    bot_user = await dp.bot.get_me()
    buy_string = await commands.get_purchases_count(message.chat.id)
    await message.answer(f"🔑 ID: {message.from_user.id}\n"
                         f"💰 Ваш баланс: {user.balance}.0 RUB\n\n"
                         f"💸 Вы купили строк: {buy_string}\n"
                         f"🎁 Бонусные строки: {user.bonus_string}\n"
                         f"🗣 Пригласили пользователей: {user.invited}\n\n"
                         f"🤝 Ваша реферальная ссылка: http://t.me/{bot_user.username}?start={message.chat.id}",
                         reply_markup=keybord_add_money, disable_web_page_preview=True)


@dp.message_handler(text="👤 Профиль", state="add_money")
async def show_menu(message: types.Message, state: FSMContext):
    await state.finish()
    bot_user = await dp.bot.get_me()
    user = await commands.select_user(message.from_user.id)
    buy_string = await commands.get_purchases_count(message.chat.id)
    await message.answer(f"🔑 ID: {message.from_user.id}\n"
                         f"💰 Ваш баланс: {user.balance}.0 RUB\n\n"
                         f"💸 Вы купили строк: {buy_string}\n"
                         f"🎁 Бонусные строки: {user.bonus_string}\n"
                         f"🗣 Пригласили пользователей: {user.invited}\n\n"
                         f"🤝 Ваша реферальная ссылка: http://t.me/{bot_user.username}?start={message.chat.id}",
                         reply_markup=keybord_add_money, disable_web_page_preview=True)


@dp.callback_query_handler(text="get_bonus_lines")
async def back_profile(call: types.CallbackQuery):
    user = await commands.select_user(call.message.chat.id)
    if user.bonus_string > 0:
        stroki = await commands.get_product(count=user.bonus_string, user_id=call.message.chat.id)
        await commands.update_bonus_string(id=call.message.chat.id)
        for u in stroki:
            await call.message.answer(u.string)
        await dp.bot.send_message(-1001657326519,
                                  f"Пользователь @{call.message.chat.username} (id:/{user.id}), получил {user.bonus_string}  бонусных строк")
    else:
        await call.message.answer(
            "У вас пока нет бонусных строк, для получения пригласите новых пользователй по вашей реферальной ссылке.\n\n"
            "За каждого приглашенного пользователя вы получите 2 строки")


@dp.callback_query_handler(text="get_lines")
async def back_profile(call: types.CallbackQuery):
    buy_string = await commands.get_purchases(call.message.chat.id)
    buy_count = await commands.get_purchases_count(call.message.chat.id)
    await call.answer(cache_time=60)
    if buy_count == 0:
        await call.message.answer("Вы пока ничего не купили")
    else:
        with open(f"documents/{call.message.chat.id}.txt", "w", encoding="UTF8") as file:
            for string in buy_string:
                updated_at = string.updated_at + dt.timedelta(hours=3)
                date = updated_at.strftime('%H:%M %d.%m.%y')
                file.write(f"{string.string} , куплен - {date}\n")

        f = open(DOC_DIR / f"{call.message.chat.id}.txt", "rb")
        await dp.bot.send_document(chat_id=call.message.chat.id, document=f)
        os.remove(f"documents/{call.message.chat.id}.txt")


@dp.callback_query_handler(text="method")
async def method_replenishment(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer(hbold("Выберите способ пополнения:"), reply_markup=keyboard_method_replenishment)


@dp.callback_query_handler(text="add_money")
async def back_profile(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()
    await call.message.answer("Введите сумму на которую хотите пополнить кошелк")
    await state.set_state("add_money")


@dp.callback_query_handler(text="back_profile", state="paid")
async def back_profile(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer(cache_time=60)
    await call.message.delete()
    bot_user = await dp.bot.get_me()
    buy_string = await commands.get_purchases_count(call.message.chat.id)
    user = await commands.select_user(call.message.chat.id)
    await call.message.answer(f"🔑 ID: {call.message.from_user.id}\n"
                              f"💰 Ваш баланс: {user.balance}.0 RUB\n\n"
                              f"💸 Вы купили строк: {buy_string}\n"
                              f"🎁 Бонусные строки: {user.bonus_string}\n"
                              f"🗣 Пригласили пользователей: {user.invited}\n\n"
                              f"🤝 Ваша реферальная ссылка: http://t.me/{bot_user.username}?start={call.message.chat.id}",
                              reply_markup=keybord_add_money, disable_web_page_preview=True)


@dp.message_handler(state="add_money")
async def update_currency(message: types.Message, state: FSMContext):
    summ = message.text
    if summ.isdigit():
        payment = Payment(amount=summ)
        payment.create()
        await message.answer(
            "\n".join(
                [
                    f"➖➖➖➖ # {payment.id}➖➖➖➖",
                    f"☎️ Кошелек для оплаты: {hcode(config.WALLET_QIWI)}",
                    f"💰 Сумма: {summ}",
                    f"💭 Комментарий: {hcode(payment.id)}",
                    f"{hbold('ВАЖНО')} Комментарий и сумма должны быть 1в1",
                    f"Ссылка: {hlink('тык', url=payment.invoice)}",
                    "➖➖➖➖➖➖➖➖➖➖➖➖",
                ]
            ),
            reply_markup=paid_keyboard
        )
        await state.set_state("paid")
        await state.update_data(payment=payment)
        await state.update_data(summ=summ)
    else:
        await message.answer("Введите корректную сумму")
        await state.set_state("add_money")


@dp.callback_query_handler(set_paid.filter(text_name="paid"), state="paid")
async def show_paid(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    data = await state.get_data()
    summ = data.get("summ")
    payment: Payment = data.get("payment")
    try:
        payment.check_payment()
    except NoPaymentFound:
        await call.message.answer("Оплата не найдена", reply_markup=paid_keyboard)

    except NotEnoughMoney:
        await call.message.answer("Не хватает денег", reply_markup=paid_keyboard)

    else:
        await commands.update_balance(id=call.message.chat.id, summ=int(summ))
        user = await commands.select_user(call.message.chat.id)
        await call.message.answer(f"Оплата прошла успешно"
                                  f"\n"
                                  f"Ваш текущий баланс: {user.balance}"
                                  ,
                                  reply_markup=main_menu)

        try:
            await dp.bot.send_message(-1001657326519,
                                      f"Пользователь @{call.message.chat.username} (id:/{user.id}) пополнил баланс на {summ}")
        except Exception as err:
            logging.exception(err)
        await state.finish()
