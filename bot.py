import telebot
import requests
import logging
import time

# =========================
# تنظیمات ربات
# =========================

BOT_TOKEN = "8766101018:AAE8n2AQCs6aMwpI3P52kPQj6KIMi6KoBVg"

# API هوش مصنوعی
AI_API_KEY = "AQ.Ab8RN6IY9M8qPSa_1uJD7l2-jkCZa4ieRD2hiThlH6DTU3kLDA"


bot = telebot.TeleBot(BOT_TOKEN)


# لاگ برای بررسی خطاها
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)



# =========================
# اتصال به هوش مصنوعی
# =========================

def ask_ai(text):

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }


    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": text
            }
        ]
    }


    try:

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )


        result = response.json()


        answer = result["choices"][0]["message"]["content"]

        return answer


    except Exception as e:

        logging.error(e)

        return "خطا در ارتباط با هوش مصنوعی"



# =========================
# دستورات ربات
# =========================


@bot.message_handler(commands=["start"])
def start(message):

    bot.reply_to(
        message,
        "سلام 👋\n"
        "من ربات هوش مصنوعی هستم.\n"
        "هر سوالی داری ارسال کن."
    )



@bot.message_handler(func=lambda m: True)
def chat(message):

    user_text = message.text


    bot.send_chat_action(
        message.chat.id,
        "typing"
    )


    answer = ask_ai(user_text)


    bot.reply_to(
        message,
        answer
    )



# =========================
# اجرای دائمی
# =========================

while True:

    try:

        print("ربات روشن شد...")

        bot.infinity_polling(
            timeout=60,
            long_polling_timeout=60
        )


    except Exception as e:

        print("خطا:", e)

        time.sleep(5)