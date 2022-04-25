# Telegram-бот магазин цифровых товаров.
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

## Описание проекта:
Разработан телеграмм бот для продажи цифровых товаров. Подключена платежная система QIWI и асинхронная база данных - PostgreSQL, реализована реферальная система, подключена админ панель.

## Настройки:

Для запуска бота нужно создать файл .env и указать: <br>
BOT_TOKEN - токен telegram-bot <br>
PGUSER - юзернейм/логин от базы данных PostgreSQL <br>
PGPASSWORD - пароль от базы данных PostgreSQL <br>
DATABASE - название базы данных <br>
QIWI_TOKEN - токен QIWI <br>
WALLET_QIWI - номер кошелька QIWI <br>
QIWI_PUBKEY - публичный ключь киви <br>
CHANNEL_ID - канал без подписки на который пользоваться ботом нельзя (указывается в виде @название канала), бот должен быть администратором в канале.

```python
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
API_KEY = str(os.getenv("API_KEY"))
API_SECRET = str(os.getenv("API_SECRET"))
PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
DATABASE = str(os.getenv("DATABASE"))
QIWI_TOKEN = str(os.getenv("qiwi"))
WALLET_QIWI = str(os.getenv("wallet"))
QIWI_PUBKEY = str(os.getenv("qiwi_p_pub"))
CHANNEL_ID = "@bonus_hunter_info"
NOTSUB_MESSAGE = "Для доступа к функционалу бота, подпишитесь на канал"
```
Так же для управления ботом указать свой чат ID в файле config.py
```python
admins = [
    #ваш чат id
]
```

Размещение товаров происходит напрямую через базу данных.<br>
Цену можно установить из админ канала.Так же в админ отображается лог покупок пользоваетелей и пополнение баланса.<br>
Можно добавлять/убавлять баланс пользователям через admin канал.<br>

## Запуск проекта

Клонируйте репозиторий: 
 
``` 
https://github.com/emuhich/strokibot.git
``` 

Перейдите в папку проекта в командной строке:

``` 
cd strokibot
``` 

Создайте и активируйте виртуальное окружение:

``` 
python -m venv venv
``` 
``` 
venv/Scripts/activate
``` 

Установите зависимости из файла *requirements.txt*: 
 
``` 
pip install -r requirements.txt
``` 
Запустите сервер:
``` 
python app.py
``` 
