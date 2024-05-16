from django.core.management.base import BaseCommand, CommandParser
from weather.models import WeatherInfo
import json
from datetime import datetime, timedelta
import requests
import pytz
import random

class Command(BaseCommand):
    help = 'Store daily weather into database'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--D',
            help='Delete all items in database',
        )
        
        parser.add_argument(
            '--U',
            action="store_true",
            help="Refresh All DailyWeather with in the specified month even existed already",
        )

        parser.add_argument(
            "--key",
            # default="feec92fecc5042f0b48e49c33529de89",
            # default="d4c9c9bc145748e48405c44277be0745",
            # default="52c4d25aafb147c5bc6e4df6cc52afc6",
            # default="7ddb2459227b4d6993afff0b4ba574ff",
            # default="f6b975aa8ad94602aefefceb2e8b3acd",
            help="Specify the key of API",
        )

        parser.add_argument(
            "--dev",
            action="store_true",
            help="Use devapi instead of api",
        )

    def handle(self, *args, **kwargs):
        if kwargs['D']:
            WeatherInfo.objects.all().delete()
        
        if kwargs["U"]:
            print("Refresh all")
        
        if kwargs['dev']:
            url = 'https://devapi.qweather.com/v7/weather/24h'
        else:
            url = 'https://api.qweather.com/v7/weather/24h'
        
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
            weather = requests.get(url, params={
                'key': kwargs['key'],
                'location': location,
            })

            weather = json.loads(weather.content.decode('utf-8'))
            # print(weather)
            for hourly in weather["hourly"]:
                date_time = datetime.fromisoformat(hourly["fxTime"])
                timezon = pytz.timezone('Asia/Shanghai')
                date_time = date_time.astimezone(timezon)

                temp_aqi = 28 + random.uniform(-10, 40)

                data = WeatherInfo(
                    # time = date_time,
                    time=timezon.localize(datetime.now()),
                    # time = datetime.now(),
                    cityName=current_city,
                    temp=hourly["temp"],
                    text=hourly["text"],
                    wind360=hourly["wind360"],
                    # windDir = hourly["windDir"],
                    windScale=hourly["windScale"],
                    windSpeed=hourly["windSpeed"],
                    humidity=hourly["humidity"],
                    precip=hourly["precip"],
                    pressure=hourly["pressure"],
                    # cloud = hourly["cloud"],
                    # dew = hourly["dew"],
                    aqi=temp_aqi,
                    category='优' if temp_aqi < 50 else '良'
                )

                data.save()

                temp_aqi = 47 + random.uniform(-40, 40)

                data = WeatherInfo(
                    # time = date_time + timedelta(days = -1),
                    time=timezon.localize(datetime.now() + timedelta(days=-1)),
                    # time = datetime.now() + timedelta(days = -1),
                    cityName=current_city,
                    temp=hourly["temp"],
                    text=hourly["text"],
                    wind360=hourly["wind360"],
                    # windDir = hourly["windDir"],
                    windScale=hourly["windScale"],
                    windSpeed=hourly["windSpeed"],
                    humidity=hourly["humidity"],
                    precip=hourly["precip"],
                    pressure=hourly["pressure"],
                    # cloud = hourly["cloud"],
                    # dew = hourly["dew"],
                    aqi=temp_aqi,
                    category='优' if temp_aqi < 50 else '良'
                )

                data.save()
            # city_name = ''
        self.stdout.write(self.style.SUCCESS('Successfully updated weather info.'))
