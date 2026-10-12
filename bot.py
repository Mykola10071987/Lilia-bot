

import os
import telebot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "Привіт! Я Ліля 🌸\n"
        "Я твій помічник. Напиши мені повідомлення!"
    )

@bot.message_handler(func=lambda message: True)
def reply(message):
    bot.reply_to(
        message,
        "Я Ліля 🌸 Отримала твоє повідомлення:\n"
        + message.text
    )

bot.infinity_polling()

