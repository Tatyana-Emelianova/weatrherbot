import requests
import datetime
from config import open_weather_token, tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands = ["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Я погодный бот. Напиши мне название города на английском и я пришлю сводку погоды")

@dp.message_handler()
async def get_weather(message: types.Message):
    code_smile = {
        "Clear": "Ясно \U0001F600",
        "Clouds" : "Облачно \U0001F642",
        "Rain": "Дождь \U0001F610",
        "Drizzle": "Дождь \U0001F610",
        "Thunderstorm": "Гроза \U0001F636",
        "Snow": "Снег \U0001F636",
        "Mist": "Туман \U0001F636",

    }

    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]
        sunrise_tinestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_tinestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        day_lenght = sunset_tinestamp - sunrise_tinestamp
        weather_desc = data["weather"][0]["main"]
        if weather_desc in code_smile:
            wd = code_smile[weather_desc]
        else:
            wd = " "

        await message.reply(f"Погода в городе: {city}\nТемпература: {cur_weather}С°{wd}\n"
        f"Влажность: {humidity} %\nДавление: {pressure} мм.рт.ст.\nСкорость_ветра: {wind_speed} м/с\n"
        f"Восход солнца: {sunrise_tinestamp}\nЗакат солнца: {sunset_tinestamp}\nПродолжительность светового дня: {day_lenght}")
        
    except:
        await message.reply("\U0001F600 проверьте название города \U0001F600")


if __name__ == "__main__":
    executor.start_polling(dp)