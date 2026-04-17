import telebot
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. ОБМАНЫВАЕМ RENDER (создаем мини-сайт для статуса "Live")
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Aura is alive!")

def run_health_check():
    # Render сам подставит нужный порт в переменную PORT
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# Запускаем "сайт" в отдельном потоке
threading.Thread(target=run_health_check, daemon=True).start()

# 2. НАСТРОЙКА БОТА
TOKEN = '8588731832:AAGHMUxp551STobX4ACSE88ryW4ywxREO3s'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Салом, BOSS! Аура теперь в полном порядке и работает автономно. 🚀")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, f"BOSS, я получила: {message.text}")

if __name__ == "__main__":
    print("--- БОТ АУРА ЗАПУЩЕН И ОБМАНУЛ СЕРВЕР ---")
    bot.infinity_polling()
