
import os
import telebot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("Не задано TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "Привіт! Я Ліля 🌸\n"
        "Я працюю! Можемо спілкуватися."
    )


@bot.message_handler(func=lambda message: True)
def reply(message):
    if message.text:
        bot.reply_to(
            message,
            "Я Ліля 🌸 Отримала твоє повідомлення:\n"
            + message.text
        )


print("Ліля запущена. Очікую повідомлення в Telegram...")
bot.infinity_polling(skip_pending=True, timeout=30)
