import json

import requests
from django.core.management.base import BaseCommand, CommandParser
from weather.models import RealtimeWeather, RealtimeAirQuality
from weather.models import City2CityId


class Command(BaseCommand):
    help = 'Store realtime weather and aqi into database'

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

        parser.add_argument(
            '--print',
            action='store_true',
            help='Print process',
        )

    def handle(self, *args, **kwargs):
        if kwargs['D']:
            print('Delete all')
            RealtimeWeather.objects.all().delete()
            RealtimeAirQuality.objects.all().delete()

        if kwargs["U"]:
            print("Refresh all")

        if kwargs['dev']:
            weather_url = 'https://devapi.qweather.com/v7/weather/now'
            air_quality_url = 'https://devapi.qweather.com/v7/air/now'
        else:
            weather_url = 'https://api.qweather.com/v7/weather/now'
            air_quality_url = 'https://api.qweather.com/v7/air/now'

        for city in City2CityId.objects.all():
            location_id = city.cityId
            city_name = city.cityName
            adm2 = city.areaName
            weather = requests.get(weather_url, params={
                'key': kwargs['key'],
                'location': location_id,
            })
            air_quality = requests.get(air_quality_url, params={
                'key': kwargs['key'],
                'location': location_id,
            })

            weather = json.loads(weather.content.decode('utf-8'))
            air_quality = json.loads(air_quality.content.decode('utf-8'))
            now_weather = weather["now"]
            now_air_quality = air_quality["now"]

            if not RealtimeWeather.objects.filter(cityName=city_name, adm2=adm2).exists():
                realtime_weather = RealtimeWeather(
                    cityName=city_name,
                    adm2=adm2,
                    temp=now_weather["temp"],
                    feelsLike=now_weather["feelsLike"],
                    icon=now_weather["icon"],
                    text=now_weather["text"],
                    wind360=now_weather["wind360"],
                    windDir=now_weather["windDir"],
                    windScale=now_weather["windScale"],
                    windSpeed=now_weather["windSpeed"],
                    humidity=now_weather['humidity'],
                    precip=now_weather["precip"],
                    pressure=now_weather["pressure"],
                )
                realtime_weather.save()

            if not RealtimeAirQuality.objects.filter(cityName=city_name, adm2=adm2).exists():
                realtime_air_quality = RealtimeAirQuality(
                    cityName=city_name,
                    adm2=adm2,
                    aqi=int(now_air_quality['aqi']),
                    level=int(now_air_quality['level']),
                    category=now_air_quality['category'],
                    pm10=now_air_quality['pm10'],
                    pm2p5=now_air_quality['pm2p5'],
                    no2=now_air_quality['no2'],
                    so2=now_air_quality['so2'],
                    co=now_air_quality['co'],
                    o3=now_air_quality['o3']
                )
                realtime_air_quality.save()

            if kwargs['print']:
                print('finish', city_name, adm2)

        self.stdout.write(self.style.SUCCESS('Successfully updated realtime weather and air quality.'))
