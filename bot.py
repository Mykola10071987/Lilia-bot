
import os
import telebot
from flask import Flask, request, abort

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")

if not TOKEN:
    raise RuntimeError("Не задано TELEGRAM_BOT_TOKEN")

if not WEBHOOK_SECRET:
    raise RuntimeError("Не задано WEBHOOK_SECRET")

if not RENDER_URL:
    raise RuntimeError("Не знайдено RENDER_EXTERNAL_URL")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


@ app.route("/", methods=["GET"])
def home():
    return "Lilia bot is running!", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    if (
        request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        != WEBHOOK_SECRET
    ):
        abort(403)

    update = telebot.types.Update.de_json(
        request.get_data().decode("utf-8")
    )
    bot.process_new_updates([update])

    return "OK", 200


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "Привіт! Я Ліля 🌸\n"
        "Приємно познайомитись!"
    )


@bot.message_handler(func=lambda message: True)
def reply(message):
    if message.text:
        bot.reply_to(
            message,
            "Я Ліля 🌸 Отримала твоє повідомлення:\n"
            + message.text
        )


bot.remove_webhook()
bot.set_webhook(
    url=f"{RENDER_URL.rstrip('/')}/webhook",
    secret_token=WEBHOOK_SECRET,
)
bot.infinity_polling()
