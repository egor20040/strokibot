from asyncpg import UniqueViolationError

from utils.db_api.db_gino import User, Product, db, Prices


async def add_user(id: int, name: str, chat_id: int, invited: int, bonus_string: int, balance: int = None,
                   purchases: str = None,
                   called: int = None):
    try:
        user = User(id=id, name=name, chat_id=chat_id, balance=balance, purchases=purchases, called=called,
                    invited=invited, bonus_string=bonus_string)

        await user.create()

    except UniqueViolationError:
        pass


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def update_balance(id: int, summ):
    user = await User.get(id)
    await user.update(balance=user.balance + summ).apply()


async def update_balance_buy(id: int, summ):
    user = await User.get(id)
    await user.update(balance=summ).apply()


async def get_count_product():
    count = await db.func.count(Product.string).gino.scalar()
    count = await Product.query.where(Product.sell == False).gino.all()
    return len(count)


async def get_purchases_count(user_id):
    count = await Product.query.where(Product.user_id == user_id).gino.all()
    return len(count)


async def get_purchases(user_id):
    count = await Product.query.where(Product.user_id == user_id).gino.all()
    return count


async def add_string(string: str):
    try:
        product = Product(string=string)

        await product.create()

    except UniqueViolationError:
        pass


async def get_product(count: int, user_id: int):
    items = await Product.query.where(Product.sell == False).limit(count).gino.all()
    for i in items:
        await i.update(sell=True, user_id=user_id).apply()
    return items


async def delete_product(count: int):
    pass
    # print(await Product.delete.limit(count).gino.status())


async def create_price():
    try:
        price = Prices(name_product='string', price=10,
                       description='🇷🇺 Строки с паспортными данными для идентификации в букмекерской конторе Фонбет')

        await price.create()

    except UniqueViolationError:
        pass


async def get_product_info(product):
    string = await Prices.query.where(Prices.name_product == product).gino.first()
    return string


async def update_price_string(price):
    string = await Prices.query.where(Prices.name_product == 'string').gino.first()
    await string.update(price=price).apply()


async def update_invited(id, invited):
    user = await User.get(id)
    await user.update(invited=invited, bonus_string=user.bonus_string + 2).apply()


async def update_bonus_string(id):
    user = await User.get(id)
    await user.update(bonus_string=0).apply()
