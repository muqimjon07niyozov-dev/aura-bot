import telebot
import os
import threading
import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. ОБМАН СЕРВЕРА RENDER (Статус Live)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Aura is Wake Up!")

def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# 2. САМО-БУДИЛЬНИК (Чтобы не засыпал без ПК)
def keep_alive():
    while True:
        try:
            # Твоя ссылка на Render
            requests.get("https://onrender.com")
            print("Будильник сработал: бот не спит")
        except:
            pass
        time.sleep(600) # Ждать 10 минут

# Запускаем всё в фоновых потоках
threading.Thread(target=run_health_check, daemon=True).start()
threading.Thread(target=keep_alive, daemon=True).start()

# 3. НАСТРОЙКА БОТА ДЛЯ BOSS
TOKEN = '8588731832:AAGHMUxp551STobX4ACSE88ryW4ywxREO3s'
MY_ID = 7758384445 # Твой ID

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id == MY_ID:
        bot.send_message(MY_ID, "Салом, BOSS! Я обновила систему 'Бессмертия'. Теперь я не усну, даже если вы выключите компьютер! 😎🚀")
    else:
        bot.send_message(message.chat.id, "Салом! Я — Аура, ваш юридический помощник. Чем могу помочь?")
        # Уведомление тебе
        bot.send_message(MY_ID, f"🔔 Новый гость: {message.from_user.first_name} (ID: {message.from_user.id})")

@bot.message_handler(func=lambda m: True)
def handle_msg(message):
    if message.chat.id != MY_ID:
        bot.send_message(MY_ID, f"📩 От {message.from_user.first_name}: {message.text}")
        bot.reply_to(message, "Ваш запрос принят. Юрист Аура анализирует информацию...")
    else:
        bot.send_message(MY_ID, "Слушаюсь, BOSS. Всё под контролем.")

if __name__ == "__main__":
    bot.infinity_polling()

