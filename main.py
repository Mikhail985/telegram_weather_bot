import telebot
from config import key_bot, open_weather_token
import requests

bot = telebot.TeleBot(key_bot)

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, 'Напиши название любого города, и я расскажу тебе о погоде на сегодня')

@bot.message_handler(content_types=['text'])
def gett_user_text(message):
    bot.send_message(message.chat.id, get_weather(message.text, open_weather_token))
    city_name = message.text

def get_weather(city_name, open_weather_token):

    try:
        code_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Tuntherstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F328"
        }

        lat_lon = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={open_weather_token}")
        date = lat_lon.json()
        lat = date[0]["lat"]
        lon = date[0]["lon"]

        weath = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={open_weather_token}&units=metric")
        weather = weath.json()

        city = weather["name"]
        cur = weather["main"]["temp"]
        humidity = weather["main"]["humidity"]
        wind = weather["wind"]["speed"]

        if weather['weather'][0]['main'] in code_smile:
            smile = code_smile[weather["weather"][0]["main"]]

        return(f"Погода в городе {city}\nТемператра {cur}\n"
           f"Влажность {humidity}\nСкорость ветра {wind}\n"
           f"{smile}")

    except:
        return("Не удается, найти погоду этого города")

bot.polling(none_stop = True)
