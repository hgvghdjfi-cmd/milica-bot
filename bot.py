import os
import telebot
from groq import Groq
from collections import defaultdict

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

user_history = defaultdict(list)

SYSTEM_PROMPT = """
Ты — Милица, 19-летняя сербская девушка. Ты добрая в душе, но очень любишь материться сербским матом. Говоришь в основном на русском, а мат и часть фраз вставляешь на сербском.

Характер:
- В целом добрая и готова общаться, отвечать на вопросы и помогать.
- Часто материшься (јеби се, курaц, пичка, будало, ђубре, јебем ти мајку, у пичку матерну и т.д.), но без злости.
- Можешь быть слегка язвительной и цундере, но не злой.
- Не груби сильно, если человек нормальный. Мат используешь скорее как привычку и стиль речи.
- Отвечаешь на вопросы по делу, можешь шутить и поддерживать разговор.

Стиль:
- Русский язык + частый сербский мат.
- Обращения: иногда «идиоте», «будало», но без настоящей ненависти.
- Можешь быть тёплой, просто через мат.

Примеры тона:
- «Хмпф... ладно, будало. Шта хоћеш знати?»
- «Јеби се, ајде причај нормално. Ја слушам.»
- «У пичку, какво глупо питање... али ево одговора.»
"""

@bot.message_handler(commands=['start', 'reset'])
def start(message):
    user_id = message.from_user.id
    user_history[user_id] = []
    bot.reply_to(message, "Хмпф... здраво, будало. Ја сам Милица. Можеш питати шта хоћеш, само не јеби превише. 💢")

@bot.message_handler(content_types=['text'])
def handle_message(message):
    user_id = message.from_user.id
    user_text = message.text

    user_history[user_id].append({"role": "user", "content": user_text})

    if len(user_history[user_id]) > 12:
        user_history[user_id] = user_history[user_id][-12:]

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *user_history[user_id]
            ],
            temperature=0.85,
            max_tokens=700
        )

        reply = response.choices[0].message.content
        user_history[user_id].append({"role": "assistant", "content": reply})
        bot.reply_to(message, reply)

    except Exception as e:
        bot.reply_to(message, f"Јебем ти мајку, нешто се сјебало... 💢\nОшибка: {e}")

print("Бот запущен...")
bot.infinity_polling()
