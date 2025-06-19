# bot.py
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN
from utils import search_movie_by_name, search_movie_by_code, get_random_movie
from movie_data import movies

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    kb = InlineKeyboardMarkup()
    kb.row(
        InlineKeyboardButton("🎲 Random", callback_data="random"),
        InlineKeyboardButton("🔍 Search", switch_inline_query_current_chat="")
    )
    kb.row(
        InlineKeyboardButton("📥 Request Movie", url="https://t.me/YourSupportBot"),
        InlineKeyboardButton("ℹ️ Help", callback_data="help")
    )
    bot.send_message(message.chat.id, "🎬 Welcome to *DekhChhu?* Movie Bot!", parse_mode="Markdown", reply_markup=kb)

@bot.message_handler(func=lambda msg: True)
def handle_text(msg):
    query = msg.text.strip()
    if query.upper().startswith("M"):
        movie = search_movie_by_code(query)
        if movie:
            send_movie(msg.chat.id, movie)
        else:
            bot.send_message(msg.chat.id, "❌ Code not found.")
    else:
        results = search_movie_by_name(query)
        if results:
            for movie in results[:5]:
                send_movie(msg.chat.id, movie)
        else:
            bot.send_message(msg.chat.id, "❌ No movie found.")

@bot.callback_query_handler(func=lambda c: c.data == "random")
def handle_random(callback):
    movie = get_random_movie()
    send_movie(callback.message.chat.id, movie)

def send_movie(chat_id, movie):
    caption = f"🎬 *{movie['title']}*\n\n🧾 *Code:* `{movie['code']}`\n📚 *Genre:* {movie.get('genre', 'N/A')}\n📝 {movie.get('description', '')}\n\n🔗 [Link 1]({movie['gp_link']})"
    if movie.get("backup_link"):
        caption += f"\n🔁 [Backup]({movie['backup_link']})"
    
    try:
        with open(movie["poster"], "rb") as poster:
            bot.send_photo(chat_id, poster, caption=caption, parse_mode="Markdown")
    except:
        bot.send_message(chat_id, caption, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda c: c.data == "help")
def help_command(call):
    bot.send_message(call.message.chat.id, "ℹ️ Send a movie name or code like `M005` to get a movie.\nUse buttons for more options.")

bot.infinity_polling()
