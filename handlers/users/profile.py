from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink, hcode
import logging

from data import config
from data.config import admins
from keyboards.default.main_menu import main_menu
from aiogram.dispatcher import FSMContext

from keyboards.inline.callback_datas import set_paid
from keyboards.inline.payment import paid_keyboard
from keyboards.inline.profile import keybord_add_money
from utils.db_api import quick_commands as commands
from loader import dp
from utils.misc.qiwi import Payment, NoPaymentFound, NotEnoughMoney


@dp.message_handler(text="Профиль")
async def show_menu(message: types.Message):
    user = await commands.select_user(message.from_user.id)
    await message.answer(f"Ваш текущий баланс: {user.balance}.0 RUB", reply_markup=keybord_add_money)


@dp.callback_query_handler(text="add_money")
async def back_profile(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите сумму на которую хотите пополнить кошелк")
    await state.set_state("add_money")


@dp.callback_query_handler(text="back_profile", state="paid")
async def back_profile(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.delete()
    user = await commands.select_user(call.message.chat.id)
    await call.message.answer(f"Ваш текущий баланс: {user.balance}.0 RUB", reply_markup=keybord_add_money)


@dp.message_handler(state="add_money")
async def update_currency(message: types.Message, state: FSMContext):
    summ = message.text
    if summ.isdigit():
        payment = Payment(amount=summ)
        payment.create()
        await message.answer(
            "\n".join(
                [
                    f"Оплатите не менее {summ} RUB по номеру телефона или по адресу",
                    "",
                    f"Ссылка: {hlink(config.WALLET_QIWI, url=payment.invoice)}",
                    "",
                    "‼️ И обязательно укажите ID платежа:",
                    hcode(payment.id)
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
        await call.message.answer("Транзакция не найдена", reply_markup=paid_keyboard)

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
        for admin in admins:
            try:
                await dp.bot.send_message(admin, f"Пользователь пополнил баланс на {summ}")

            except Exception as err:
                logging.exception(err)
        await state.finish()
