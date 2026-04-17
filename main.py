import telebot
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. ОБМАН СЕРВЕРА RENDER (чтобы статус был "Live" и бот не засыпал)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"BOSS, Aura is monitoring everything!")

def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

threading.Thread(target=run_health_check, daemon=True).start()

# 2. НАСТРОЙКИ БОТА И BOSS-КОНТРОЛЬ
TOKEN = '8588731832:AAGHMUxp551STobX4ACSE88ryW4ywxREO3s'
MY_ID = 7758384445 # Твой подтвержденный ID

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    # Если зашел ТЫ (BOSS)
    if message.chat.id == MY_ID:
        bot.send_message(MY_ID, "Приветствую, BOSS! Система мониторинга активна. Я буду слать вам отчеты о всех гостях.")
    # Если зашел КТО-ТО ДРУГОЙ
    else:
        welcome_text = "Салом! Я — Аура, ваш юридический помощник в Таджикистане. Задайте свой вопрос."
        bot.send_message(message.chat.id, welcome_text)
        # Сразу уведомляем тебя
        report = f"🔔 **Новый гость в боте!**\n👤 Имя: {message.from_user.first_name}\n🆔 ID: {message.from_user.id}\n🔗 Юзернейм: @{message.from_user.username}"
        bot.send_message(MY_ID, report, parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def handle_messages(message):
    # Если пишет НЕ BOSS, пересылаем сообщение тебе
    if message.chat.id != MY_ID:
        log_text = f"📩 **Сообщение от {message.from_user.first_name}:**\n\"{message.text}\""
        bot.send_message(MY_ID, log_text, parse_mode="Markdown")
        
        # Ответ пользователю (имитация юриста)
        bot.reply_to(message, "Ваш запрос принят. Юрист Аура анализирует информацию...")
    else:
        # Если пишешь ты сам, бот просто подтверждает
        bot.send_message(MY_ID, "Принято, BOSS. Жду новых гостей.")

if __name__ == "__main__":
    print("--- МОНИТОРИНГ БОССА ЗАПУЩЕН ---")
    bot.infinity_polling()
