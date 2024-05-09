from django.core.management.base import BaseCommand
from weather.models import DailyWeather
import json
from datetime import datetime
import requests
import pytz
import random

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        DailyWeather.objects.all().delete()
        weather = requests.get('https://devapi.qweather.com/v7/weather/30d', params={
            'key': 'aa7975af7b564c60804b6b08fab2e2c5',
            'location': '101010100',
        })

        weather = json.loads(weather.content.decode('utf-8'))
        # print(weather)
        for daily in weather["daily"]:
            date_time = datetime.fromisoformat(daily["fxTime"])
            timezon = pytz.timezone('Asia/Shanghai')
            date_time = date_time.astimezone(timezon)

            temp_aqi = random.randint(10, 150)

            data = DailyWeather(
                # time = date_time,
                time = timezon.localize(datetime.now()),
                # time = datetime.now(),
                city = '北京市',
                tempMax = daily["tempMax"],
                tempMin = daily["tempMin"],
                humidity = daily["humidity"],
                precip = daily["precip"],
                pressure = daily["pressure"],
                cloud = daily["cloud"],
                # dew = hourly["dew"],
                aqi = temp_aqi,
                # category = '优' if temp_aqi < 50 else '良'
            )

            data.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated monthly weather info.'))