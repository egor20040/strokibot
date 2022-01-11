from aiogram import types

from data.config import CHANNEL_ID, NOTSUB_MESSAGE
from handlers.users.products import check_sub_channel
from keyboards.inline.channel_subscription import subscription_keyboard
from loader import dp


@dp.message_handler(text="💬 Обратная связь")
async def show_menu(message: types.Message):
    if check_sub_channel(await dp.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)):
        text = [
            ' Если у вас возникли вопросы по товарам, а так же,если у вас попался товар не соответствующий описанию товара. То писать сюда : @suneeni',
        ]
        await message.answer('\n'.join(text))
    else:
        await message.answer(NOTSUB_MESSAGE, reply_markup=subscription_keyboard)
