from asyncpg import UniqueViolationError

from utils.db_api.db_gino import User, Product


async def add_user(id: int, name: str, chat_id: int, balance: int = None, purchases: str = None, ):
    try:
        user = User(id=id, name=name, chat_id=chat_id, balance=balance, purchases=purchases)

        await user.create()

    except UniqueViolationError:
        pass


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def update_balance(id: int, summ):
    user = await User.get(id)
    balance = user.balance + summ
    await user.update(balance=balance).apply()


async def update_balance_buy(id: int, summ):
    user = await User.get(id)
    await user.update(balance=summ).apply()


async def add_string(string: str):
    try:
        product = Product(string=string)

        await product.create()

    except UniqueViolationError:
        pass
