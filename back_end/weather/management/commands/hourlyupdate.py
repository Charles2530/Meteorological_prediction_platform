from django.core.management.base import BaseCommand
from weather.models import WeatherInfo
import json
from datetime import datetime, timedelta
import requests
import pytz

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        weather = requests.get('https://devapi.qweather.com/v7/weather/24h', params={
            'key': '7ddb2459227b4d6993afff0b4ba574ff',
            'location': "101010100", ## Beijing
        })

        weather = json.loads(weather.content.decode('utf-8'))
        # print(weather)
        for hourly in weather["hourly"]:
            date_time = datetime.fromisoformat(hourly["fxTime"])
            timezon = pytz.timezone('Asia/Shanghai')
            date_time = date_time.astimezone(timezon)

            data = WeatherInfo(
                time = date_time,
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
            )

            data.save()

            data = WeatherInfo(
                time = date_time + timedelta(days = -1),
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
            )

            data.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated weather info.'))