from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import CHANNEL_ID, NOTSUB_MESSAGE
from keyboards.default.main_menu import main_menu
from keyboards.inline.channel_subscription import subscription_keyboard
from keyboards.inline.products import keybord_products
from keyboards.inline.profile import keybord_add_money
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


@dp.callback_query_handler(text="back_menu")
async def back_profile(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer("Выберете категорию которая вам нужна ниже:", reply_markup=main_menu)


@dp.message_handler(text='Отмена')
async def main_menu(message: types.Message):
    await message.answer("Выберете категорию которая вам нужна ниже:", reply_markup=main_menu)


@dp.message_handler(text="👤 Профиль", state='*')
async def show_menu(message: types.Message, state: FSMContext):
    await state.finish()
    if check_sub_channel(await dp.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        user = await commands.select_user(message.from_user.id)
        buy_string = await commands.get_purchases_count(message.chat.id)
        bot_user = await dp.bot.get_me()
        await message.answer(f"🔑 ID: {message.from_user.id}\n"
                             f"💰 Ваш баланс: {user.balance}.0 RUB\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                             f"💸 Вы купили строк: {buy_string}\n"
                             f"🎁 Бонусные строки: {user.bonus_string}\n"
                             f"🗣 Пригласили пользователей: {user.invited}\n"
                             "➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                             f"🤝 Ваша реферальная ссылка: http://t.me/{bot_user.username}?start={message.chat.id}",
                             reply_markup=keybord_add_money, disable_web_page_preview=True)
    else:
        await message.answer(NOTSUB_MESSAGE, reply_markup=subscription_keyboard)


@dp.message_handler(text="📖 Наличие товаров", state='*')
async def show_menu(message: types.Message, state: FSMContext):
    await state.finish()
    if check_sub_channel(await dp.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        await message.answer("Выберете товар, который хотите купить:", reply_markup=keybord_products)
    else:
        await message.answer(NOTSUB_MESSAGE, reply_markup=subscription_keyboard)


@dp.message_handler(text="💬 Обратная связь", state='*')
async def show_menu(message: types.Message, state: FSMContext):
    await state.finish()
    if check_sub_channel(await dp.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        text = [
            ' Если у вас возникли вопросы по товарам, а так же,если у вас попался товар не соответствующий описанию товара. То писать сюда : @suneeni',
        ]
        await message.answer('\n'.join(text))
    else:
        await message.answer(NOTSUB_MESSAGE, reply_markup=subscription_keyboard)
