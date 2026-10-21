
import os
import time
import logging
import telebot
from openai import OpenAI

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not TOKEN:
    raise RuntimeError("Не задано TELEGRAM_BOT_TOKEN")

if not GROQ_API_KEY:
    raise RuntimeError("Не задано GROQ_API_KEY")

bot = telebot.TeleBot(TOKEN)

ai = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)


def ask_lilia(question):
    response = ai.responses.create(
        model="llama-3.3-70b-versatile",
        instructions=(
            "Ти Ліля, доброзичлива розумна помічниця. "
            "Відповідай українською мовою, природно, "
            "зрозуміло та по суті. "
            "Якщо не знаєш відповіді, чесно скажи про це. "
            "Не вигадуй факти."
        ),
        input=question
    )
    return response.output_text.strip()


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "Привіт! Я Ліля 🌸\n"
        "Я працюю через Groq. "
        "Напиши, що тебе цікавить."
    )


@bot.message_handler(content_types=["text"])
def reply(message):
    question = message.text.strip()

    if not question:
        return

    status = bot.reply_to(message, "Зараз подумаю 🌸")

    try:
        answer = ask_lilia(question)

        if not answer:
            answer = "Не вдалося сформувати відповідь. Спробуй ще раз."

        chunks = [
            answer[i:i + 4000]
            for i in range(0, len(answer), 4000)
        ]

        bot.edit_message_text(
            chunks[0],
            chat_id=message.chat.id,
            message_id=status.message_id
        )

        for chunk in chunks[1:]:
            bot.send_message(message.chat.id, chunk)

    except Exception:
        logging.exception("Помилка відповіді Лілі")
        try:
            bot.edit_message_text(
                "Вибач, зараз не вдалося отримати відповідь. "
                "Спробуй трохи пізніше 🌸",
                chat_id=message.chat.id,
                message_id=status.message_id
            )
        except Exception:
            logging.exception("Не вдалося надіслати повідомлення про помилку")


print("Ліля запущена через Groq. Очікую повідомлення в Telegram...")

while True:
    try:
        print("Ліля підключається до Telegram...")
        bot.infinity_polling(
            skip_pending=True,
            timeout=30,
            long_polling_timeout=25
        )
    except Exception:
        logging.exception("Помилка з'єднання Лілі")
        time.sleep(5)
