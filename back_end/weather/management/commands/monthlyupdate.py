from django.core.management.base import BaseCommand, CommandParser
from weather.models import DailyWeather
import json
from datetime import datetime
import requests
import pytz
import random


class Command(BaseCommand):
    help = 'Store daily weather into database'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--D',
            action='store_true',
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
            print('Delete all')
            DailyWeather.objects.all().delete()

        if kwargs["U"]:
            print("Refresh all")

        if kwargs['dev']:
            url = 'https://devapi.qweather.com/v7/weather/7d'
        else:
            url = 'https://api.qweather.com/v7/weather/7d'

        weather = requests.get(url, params={
            'key': kwargs['key'],
            'location': '101010100',
        })

        weather = json.loads(weather.content.decode('utf-8'))
        # print(weather)
        for daily in weather["daily"]:
            date_time = datetime.fromisoformat(daily["fxDate"])
            timezon = pytz.timezone('Asia/Shanghai')
            date_time = date_time.astimezone(timezon)

            temp_aqi = random.randint(10, 150)  # TODO

            data = DailyWeather(
                # time = date_time,
                fxDate=timezon.localize(datetime.now()),
                # time = datetime.now(),
                city='北京市',
                sunrise=daily["sunrise"],
                sunset=daily["sunset"],
                tempMax=daily["tempMax"],
                tempMin=daily["tempMin"],
                humidity=daily["humidity"],
                windSpeedDay=daily["windSpeedDay"],
                precip=daily["precip"],
                pressure=daily["pressure"],
                cloud=daily["cloud"],
                # dew = hourly["dew"],
                aqi=temp_aqi,
                # category = '优' if temp_aqi < 50 else '良'
            )

            data.save()
        self.stdout.write(self.style.SUCCESS('Successfully updated monthly weather info.'))
