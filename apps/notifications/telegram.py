import os

from telegram import Bot

BOT_TOKEN = os.environ.get("redis://localhost:6379/0")
ADMIN_CHAT_ID = os.environ.get("568925603")

bot = Bot(token=BOT_TOKEN)

def send_message(text: str):
    bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)