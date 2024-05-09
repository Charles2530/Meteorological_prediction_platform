from django.core.management.base import BaseCommand
from weather.models import HourlyWeather
from datetime import datetime
import request

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        weather = requests.get('https://api.qweather.com/v7/weather/72h', params={
            'key': '52c4d25aafb147c5bc6e4df6cc52afc6',
            'location': "101010100", ## Beijing
        })

        weather = json.loads(weather.content.decode('utf-8'))

        for hourly in weather["hourly"]:
            date_time = datetime.fromisoformat(hourly["fxTime"])
            timezon = pytz.timezone('Asia/Shanghai')
            date_time = date_time.astimezone(timezon)

            data = HourlyWeather(
                fxTime = date_time,
                temp = hourly["temp"],
                icon = hourly["icon"],
                text = hourly["text"],
                wind360 = hourly["wind360"],
                windDir = hourly["windDir"],
                windScale = hourly["windScale"],
                windSpeed = hourly["windSpeed"],
                humidity = hourly["humidity"],
                pop = hourly["pop"],
                precip = hourly["precip"],
                pressure = hourly["pressure"],
                cloud = hourly["cloud"],
                dew = hourly["dew"],
            )

            data.save()
