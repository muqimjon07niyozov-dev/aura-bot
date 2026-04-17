import telebot

# Твой токен
TOKEN = '8588731832:AAGHMUxp551STobX4ACSE88ryW4ywxREO3s'
# Твой личный ID (чтобы бот знал, кому слать отчеты). 
# Узнай свой ID у бота @userinfobot и впиши сюда вместо 000000
ADMIN_ID = 5602525128 # Впиши сюда свой цифровой ID

bot = telebot.TeleBot(TOKEN)

# Функция для проверки документов (имитация логики для Таджикистана)
def check_document_logic(text):
    if len(text) == 9 and text[0].isalpha(): # Пример: A12345678
        return "✅ Похоже на номер загранпаспорта РТ. Проверяю в базе..."
    return "ℹ️ Отправьте номер документа для проверки (например, загранпаспорт)."

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Салом, BOSS! Я Аура. Отправьте номер документа РТ для проверки.")
    # Уведомление админу о новом пользователе
    bot.send_message(ADMIN_ID, f"🔔 Новый пользователь!\nИмя: {message.from_user.first_name}\nID: {message.from_user.id}")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    # 1. Логируем сообщение для тебя (BOSS)
    log_text = f"👤 От: {message.from_user.first_name} (ID: {message.from_user.id})\n💬 Написал: {message.text}"
    bot.send_message(ADMIN_ID, log_text)

    # 2. Логика проверки документов
    response = check_document_logic(message.text)
    bot.reply_to(message, response)

if __name__ == "__main__":
    print("--- БОТ АУРА С ЛОГАМИ ЗАПУЩЕН ---")
    bot.infinity_polling()
