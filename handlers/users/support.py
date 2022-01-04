from aiogram import types

from loader import dp


@dp.message_handler(text="💬 Обратная связь")
async def show_menu(message: types.Message):
    text = [
        ' Если у вас возникли вопросы по товарам, а так же,если у вас попался товар не соответствующий описанию товара. То писать сюда : @suneeni',
    ]
    await message.answer('\n'.join(text))
