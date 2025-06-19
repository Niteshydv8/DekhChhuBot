import telebot
import os

# 🔐 Replace with your real values
BOT_TOKEN = "8033001363:AAHAHNo-Vpjb5vLW7xjW_tNLWSz7Odwqs7c"
CHAT_ID = "5762701937"

POSTER_FOLDER = "posters"

bot = telebot.TeleBot(BOT_TOKEN)

for filename in os.listdir(POSTER_FOLDER):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        filepath = os.path.join(POSTER_FOLDER, filename)
        movie_name = filename.replace("_", " ").replace(".jpg", "").title()
        with open(filepath, "rb") as poster:
            print(f"Sending: {movie_name}")
            bot.send_photo(chat_id=CHAT_ID, photo=poster, caption=movie_name)

print("✅ All posters sent.")
