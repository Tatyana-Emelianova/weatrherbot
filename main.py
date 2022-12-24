import requests
from pprint import pprint
import datetime
from config import open_weather_token

def get_weather (city, open_weather_token):
    
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
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        pprint(data)

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

        print(f"Погода в городе: {city}\nТемпература: {cur_weather}С°{wd}\n"
        f"Влажность: {humidity} %\nДавление: {pressure} мм.рт.ст.\nСкорость_ветра: {wind_speed} м/с\n"
        f"Восход солнца: {sunrise_tinestamp}\nЗакат солнца: {sunset_tinestamp}\nПродолжительность светового дня: {day_lenght}")
        
    except Exception as ex:
        print(ex)
        print("проверьте название города")

def main():
    city = input("введите город: ")
    get_weather(city, open_weather_token)

if __name__ == "__main__":
    main()