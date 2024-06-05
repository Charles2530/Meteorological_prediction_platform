from django.core.management.base import BaseCommand, CommandParser
from weather.models import WeatherInfo, City2CityId
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
            action='store_true',
            help='Delete all items in database',
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
            WeatherInfo.objects.all().delete()

        if kwargs['dev']:
            url = 'https://devapi.qweather.com/v7/weather/168h'
        else:
            url = 'https://api.qweather.com/v7/weather/168h'

        for location_int in range(101010100, 101011800, 100):
            location_id = str(location_int)
            weather = requests.get(url, params={
                'key': kwargs['key'],
                'location': location_id,
            })

            city = City2CityId.objects.get(cityId=location_id)
            city_name = city.cityName
            adm2 = city.areaName

            print('-----', city_name, '-', adm2, '-----', 'in hourly update')

            weather = json.loads(weather.content.decode('utf-8'))
            # print(weather)
            for hourly in weather["hourly"]:
                shanghai_timezone = pytz.timezone('Asia/Shanghai')
                dt = datetime.fromisoformat(hourly["fxTime"]).astimezone(shanghai_timezone)
                rounded_dt = dt.replace(minute=0, second=0, microsecond=0)

                temp_aqi = 28 + random.uniform(-10, 40)

                data = WeatherInfo(
                    time=rounded_dt,
                    cityName=city_name,
                    adm2=adm2,
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

                rounded_former_time = (datetime.now() + timedelta(days=-1)).replace(minute=0, second=0, microsecond=0)

                data = WeatherInfo(
                    time=shanghai_timezone.localize(rounded_former_time),
                    cityName=city_name,
                    adm2=adm2,
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
