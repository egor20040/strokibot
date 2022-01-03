from typing import List

from aiogram import Dispatcher
from gino import Gino
import sqlalchemy as sa
from sqlalchemy import Integer, Column, String, DateTime, BigInteger, sql, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from data import config

db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimeBaseModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=db.func.now())
    updated_at = Column(DateTime(True), default=db.func.now(),
                        onupdate=db.func.now(),
                        server_default=db.func.now())


class User(TimeBaseModel):
    __tablename__ = 'users'
    query: sql.Select
    id = Column(BigInteger, primary_key=True)
    name = Column(String(100))
    chat_id = Column(BigInteger)
    balance = Column(Integer)
    purchases = Column(String(100))


class Product(TimeBaseModel):
    __tablename__ = 'product'
    query: sql.Select
    id = Column(Integer, primary_key=True)
    string = Column(String(100))
    sell = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))


class Prices(TimeBaseModel):
    __tablename__ = 'price'
    query: sql.Select
    id = Column(Integer, primary_key=True)
    name_product = Column(String(100))
    price = Column(Integer)


async def on_startup(dispatcher: Dispatcher):
    print("Установка связи с PostgreSQL")
    await db.set_bind(config.POSTGRES_URL)
    print("Готово")
    print("Создаем таблицу")
    await db.gino.create_all()
    print("Готово")
