import telebot
import telebot as tl
import requests as rq
import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
weather_token = os.getenv('WEATHER_TOKEN')
admin_id = os.getenv('ADMIN_ID')

bot = tl.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def welcome(message):
    msg = message.chat.id
    bot.send_message(msg, f'Привіт, {message.from_user.first_name}тебе вітає бот, який допоможе тобі дізнатися прогноз погоди в любій частинці світу.')
    bot.send_message(msg, 'Нижче напиши місто, в якому ти б хотів дізнатися прогноз погоди')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text
    msg = message.chat.id

    try:
        admin_msg = f'🕵️ {message.from_user.first_name} (ID: {message.from_user.id}) шукає: {city}'
        bot.send_message(admin_id, admin_msg)
    except Exception as e:
        print(f"Не вдалося відправити лог: {e}")

    bot.send_message(msg, f'Триває пошук погоди для міста {city}..')

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_token}&units=metric&lang=ua"

    try:
        response = rq.get(url)
        data = response.json()
        if data['cod'] == 200:
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            description = data['weather'][0]['description']
            temp_min = data['main']['temp_min']
            temp_max = data['main']['temp_max']

            reply = (
                f'Погода у місті {city.capitalize()}:\n'
                f'Температура: {round(temp)}°C, а відчувається як {round(feels_like)}. Передбачається {description.lower()}\n'
                f'Мінімальна температура сьогодні: {round(temp_min)}°C, сягає до {round(temp_max)}°C'
            )
            bot.reply_to(message, reply)
        else:
            bot.reply_to(message, 'Місто не знайдено. Перевір правильність написання та спробуй ще раз!')
    except Exception as e:
        bot.reply_to(message, 'Виникла помилка при отриманні даних. Спробуй пізніше')

bot.polling(none_stop=True)

