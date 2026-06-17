import os
import telebot
from telebot import types
from flask import Flask, request

TOKEN = '8879633069:AAG36ovFiIygP6HDkPCDIZGqWnOq64Jb-WA'
# Вставь сюда URL, который тебе выдаст Render после создания сервиса (например, https://my-bot.onrender.com)
RENDER_URL = 'https://твой-сабдомен.onrender.com' 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.InlineKeyboardMarkup()
    
    app_furniture = types.WebAppInfo("https://твой-альфурат.netlify.app")
    app_weather = types.WebAppInfo("https://твоя-погода-react.netlify.app")
    app_landing = types.WebAppInfo("https://твой-маджента-ленд.netlify.app")
    
    btn_furniture = types.InlineKeyboardButton(text="🪑 Мебельный Fullstack (Alfurat)", web_app=app_furniture)
    btn_weather = types.InlineKeyboardButton(text="🌤 Приложение Погоды (React SPA)", web_app=app_weather)
    btn_landing = types.InlineKeyboardButton(text="🔮 Современный Лендинг (HTML/CSS/JS)", web_app=app_landing)
    
    markup.add(btn_furniture)
    markup.add(btn_weather)
    markup.add(btn_landing)
    
    bot.send_message(
        message.chat.id, 
        f"Привет, {message.from_user.first_name}! 👋\n\nВыбери интересующий сайт ниже 👇", 
        reply_markup=markup
    )

# Эндпоинт для приема уведомлений от Telegram
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# Главная страница (чтобы Render видел, что сервис жив)
@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + '/' + TOKEN)
    return "Бот-портал работает через вебхук!", 200

if __name__ == "__main__":
    # Локальный запуск для тестов
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))