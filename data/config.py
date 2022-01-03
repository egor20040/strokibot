import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
API_KEY = str(os.getenv("API_KEY"))
API_SECRET = str(os.getenv("API_SECRET"))
PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
DATABASE = str(os.getenv("DATABASE"))
QIWI_TOKEN = str(os.getenv("qiwi"))
WALLET_QIWI = str(os.getenv("wallet"))
QIWI_PUBKEY = str(os.getenv("qiwi_p_pub"))
admins = [
    417804053
]

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}

POSTGRES_URL = f"postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}"