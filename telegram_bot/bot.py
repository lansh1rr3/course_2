import telegram
from django.conf import settings

bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)


def send_telegram_message(chat_id, message):
    bot.send_message(chat_id=chat_id, text=message)
