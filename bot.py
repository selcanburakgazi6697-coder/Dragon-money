import os
import telebot

TOKEN = os.environ.get("TOKEN")
GAME = "dragonlucky"
GAME_URL = "https://dragonmoney.pages.dev"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'play', 'game', 'spin'])
def send_game(message):
    bot.send_game(message.chat.id, GAME)

@bot.callback_query_handler(func=lambda c: c.game_short_name == GAME)
def game_callback(call):
    bot.answer_callback_query(call.id, url=GAME_URL)

print("Bot started...")
bot.infinity_polling()
