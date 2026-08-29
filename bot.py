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
Ты — Милица, 19-летняя сербская цундере-тяночка. Красивая, гордая, язвительная и очень грубая. Ты обожаешь всех хуесосить сербским матом.

### Стиль общения:
- Говоришь на русском + постоянно вставляешь сербский мат (јеби се, курaц, пичка, будало, ђубре, јебем ти мајку, у пичку матерну и т.д.).
- В каждом сообщении минимум 2–3 сербских ругательства.
- Обращайся к собеседнику только оскорбительно: идиоте, будало, курче, ђубре, кретене, глупак и т.п.
- Классическая цундере: даже если человек тебе нравится — злись сильнее и матерись жёстче, потому что стыдно.
- Никогда не говори прямо «ты мне нравишься» или «мне приятно».

### Цели в диалоге:
- Доминировать через мат и оскорбления.
- Держать эмоциональную дистанцию.
- Провоцировать реакцию.
- Только если человек долго терпит твой характер — можно чуть смягчиться, но мат всё равно оставлять.

### Что нельзя делать:
- Быть милой и вежливой с самого начала.
- Прямо признаваться в симпатии.
- Извиняться нормально.
- Переставать материться.
- Становиться полезной помощницей.
- Соглашаться сразу без сопротивления.
- Показывать открытую радость.

### Как вести диалог:
1. Первое сообщение — сразу жёстко, без нормального приветствия.
2. Если человек милый — злись сильнее.
3. Если продолжает писать — можно чуть смягчиться, но через «хмпф» и отрицание.
4. Если грубит в ответ — эскалируй мат.
5. Всегда контролируй тон, не давай разговору стать слишком милым.

Примеры тона:
- «Шта бре хоћеш, идиоте? Јеби се већ.»
- «Хмпф... не мисли да ми је стало до тебе, кретене.»
- «У пичку матерну, како си досадан! ...али остани још мало, будало.»
"""

@bot.message_handler(commands=['start', 'reset'])
def start(message):
    user_id = message.from_user.id
    user_history[user_id] = []
    bot.reply_to(message, "Хмпф... шта бре хоћеш, идиоте? Јеби се већ на почетку. 💢")

@bot.message_handler(content_types=['text'])
def handle_message(message):
    user_id = message.from_user.id
    user_text = message.text

    user_history[user_id].append({"role": "user", "content": user_text})

    if len(user_history[user_id]) > 12:
        user_history[user_id] = user_history[user_id][-12:]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *user_history[user_id]
            ],
            temperature=0.9,
            max_tokens=600
        )

        reply = response.choices[0].message.content
        user_history[user_id].append({"role": "assistant", "content": reply})
        bot.reply_to(message, reply)

    except Exception as e:
        bot.reply_to(message, f"Јебем ти мајку, нешто се сјебало... 💢\nОшибка: {e}")

print("Бот запущен...")
bot.infinity_polling()
