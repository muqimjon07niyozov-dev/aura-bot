import telebot

TOKEN = '8588731832:AAGHMUxp551STobX4ACSE88ryW4ywxREO3s'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "BOSS, я на связи! Теперь я работаю на Render автономно. 😎")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, f"BOSS, ты написал: {message.text}")

if __name__ == "__main__":
    bot.infinity_polling()
