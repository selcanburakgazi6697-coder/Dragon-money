import os
import requests
import telebot

TOKEN = os.environ.get("TOKEN")
GAME = "dragonslot"
GAME_URL = "https://dragonmoney.pages.dev"

STATS_URL = "https://dragon-stats.selcanburakgazi6697.workers.dev"
STATS_KEY = "dragon2026stats"
ADMIN_IDS = [YOUR_TELEGRAM_ID]  # замени на свой ID

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'play', 'game', 'spin'])
def send_game(message):
    bot.send_game(message.chat.id, GAME)

@bot.callback_query_handler(func=lambda c: c.game_short_name == GAME)
def game_callback(call):
    bot.answer_callback_query(call.id, url=GAME_URL)

@bot.message_handler(commands=['stats'])
def send_stats(message):
    if message.from_user.id not in ADMIN_IDS:
        return
    try:
        r = requests.get(f"{STATS_URL}/stats", params={"key": STATS_KEY}, timeout=5)
        d = r.json()
        text = (
            f"📊 Dragon Lucky Spin — Статистика\n\n"
            f"Всего:\n"
            f"  👁 Визитов: {d['total']['visits']}\n"
            f"  🎰 Спинов: {d['total']['spins']}\n"
            f"  🔗 Кликов: {d['total']['clicks']}\n\n"
            f"Уникальных:\n"
            f"  👤 Посетителей: {d['unique']['visits']}\n"
            f"  🔗 Перешли: {d['unique']['clicks']}\n\n"
            f"Сегодня:\n"
            f"  👁 Визитов: {d['today']['visits']}\n"
            f"  🎰 Спинов: {d['today']['spins']}\n"
            f"  🔗 Кликов: {d['today']['clicks']}\n\n"
            f"📈 CTR: {d['ctr']}"
        )
        bot.send_message(message.chat.id, text)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

print("Bot started...")
bot.infinity_polling()
