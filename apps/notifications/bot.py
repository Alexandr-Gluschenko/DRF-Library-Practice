import asyncio
from telegram import Bot

BOT_TOKEN = "8184100062:AAFlIARCwhDVv-TrtoFmZTbF9iz91TKq_Rs"
ADMIN_CHAT_ID = 568925603

bot = Bot(token=BOT_TOKEN)

async def send_message(text: str):
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)

if __name__ == "__main__":
    asyncio.run(send_message("The bot is working ✅"))
