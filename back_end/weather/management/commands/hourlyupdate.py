from django.core.management.base import BaseCommand
from weather.models import WeatherInfo
import json
from datetime import datetime, timedelta
import requests
import pytz
import random

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        WeatherInfo.objects.all().delete()
        target_locations = ['101010100',  # Beijing
                            '101020100',  # Shanghai
                            '101030100',  # Tianjin
                            '101040100'   # Chongqing
                            ]
        target_cities = [
            '北京市',
            '上海市',
            '天津市',
            '重庆市'
        ]
        for location, current_city in zip(target_locations, target_cities):
            weather = requests.get('https://devapi.qweather.com/v7/weather/24h', params={
                'key': '7ddb2459227b4d6993afff0b4ba574ff',
                'location': location,
            })

            weather = json.loads(weather.content.decode('utf-8'))
            # print(weather)
            for hourly in weather["hourly"]:
                date_time = datetime.fromisoformat(hourly["fxTime"])
                timezon = pytz.timezone('Asia/Shanghai')
                date_time = date_time.astimezone(timezon)

                temp_aqi = 28 + random.uniform(-40, 40)

                data = WeatherInfo(
                    # time = date_time,
                    time = timezon.localize(datetime.now()),
                    # time = datetime.now(),
                    city = current_city,
                    temp = hourly["temp"],
                    text = hourly["text"],
                    wind360 = hourly["wind360"],
                    # windDir = hourly["windDir"],
                    windScale = hourly["windScale"],
                    windSpeed = hourly["windSpeed"],
                    humidity = hourly["humidity"],
                    precip = hourly["precip"],
                    pressure = hourly["pressure"],
                    # cloud = hourly["cloud"],
                    # dew = hourly["dew"],
                    aqi = temp_aqi,
                    category = '优' if temp_aqi < 50 else '良'
                )

                data.save()

                temp_aqi = 47 + random.uniform(-40, 40)

                data = WeatherInfo(
                    # time = date_time + timedelta(days = -1),
                    time = timezon.localize(datetime.now() + timedelta(days = -1)),
                    # time = datetime.now() + timedelta(days = -1),
                    city = current_city,
                    temp = hourly["temp"],
                    text = hourly["text"],
                    wind360 = hourly["wind360"],
                    # windDir = hourly["windDir"],
                    windScale = hourly["windScale"],
                    windSpeed = hourly["windSpeed"],
                    humidity = hourly["humidity"],
                    precip = hourly["precip"],
                    pressure = hourly["pressure"],
                    # cloud = hourly["cloud"],
                    # dew = hourly["dew"],
                    aqi = temp_aqi,
                    category = '优' if temp_aqi < 50 else '良'
                )

                data.save()
            # city_name = ''
        self.stdout.write(self.style.SUCCESS('Successfully updated weather info.'))