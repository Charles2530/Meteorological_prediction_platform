from django.core.management.base import BaseCommand, CommandParser
from weather.models import DailyWeather, City2CityId
import json
from datetime import date, datetime, timedelta
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

        parser.add_argument(
            '--print',
            action='store_true',
            help='Print process',
        )

    def handle(self, *args, **kwargs):
        if kwargs['D']:
            print('Delete all')
            DailyWeather.objects.all().delete()

        if kwargs["U"]:
            print("Refresh all")

        if kwargs['dev']:
            historic_url = ''
            url = 'https://devapi.qweather.com/v7/weather/7d'
        else:
            historic_url = 'https://api.qweather.com/v7/historical/weather'
            url = 'https://api.qweather.com/v7/weather/30d'

        shanghai_timezone = pytz.timezone('Asia/Shanghai')

        if DailyWeather.objects.count() > 0:
            # delete incomplete data
            city_name = DailyWeather.objects.last().city
            adm2 = DailyWeather.objects.last().adm2
            DailyWeather.objects.filter(city=city_name, adm2=adm2).delete()

        for city in City2CityId.objects.all():
            location_id = city.cityId
            city_name = city.cityName
            adm2 = city.areaName

            if DailyWeather.objects.filter(city=city_name, adm2=adm2).exists():
                print(city_name, adm2, 'already exists')
                continue

            if not kwargs['dev']:
                for i in range(-9, 0):
                    query_date = date.today() + timedelta(days=i)

                    while True:
                        historic_weather = requests.get(historic_url, params={
                            'key': kwargs['key'],
                            'location': location_id,
                            'date': query_date.strftime('%Y%m%d')
                        })
                        historic_weather = json.loads(historic_weather.content.decode('utf-8'))
                        if historic_weather['code'] == '429':
                            print("wait to access")
                            time.sleep(30)
                            continue
                        break

                    if historic_weather['code'] == '404':
                        continue
                    # print('historic_weather', historic_weather)

                    daily = historic_weather["weatherDaily"]
                    temp_date_time = datetime.strptime(daily['date'], '%Y-%m-%d')
                    date_time = temp_date_time.astimezone(shanghai_timezone)

                    temp_aqi = random.randint(10, 150)  # TODO
                    temp_wind_speed = random.randint(1, 7)  # TODO

                    data = DailyWeather(
                        fxDate=date_time,
                        city=city_name,
                        adm2=adm2,
                        sunrise=daily["sunrise"],
                        sunset=daily["sunset"],
                        tempMax=daily["tempMax"],
                        tempMin=daily["tempMin"],
                        humidity=daily["humidity"],
                        windSpeedDay=temp_wind_speed,
                        precip=daily["precip"],
                        pressure=daily["pressure"],
                        aqi=temp_aqi,
                        # category = '优' if temp_aqi < 50 else '良'
                    )

                    data.save()

            while True:
                weather = requests.get(url, params={
                    'key': kwargs['key'],
                    'location': location_id,
                })
                weather = json.loads(weather.content.decode('utf-8'))
                if weather['code'] == '429':
                    print("wait to access")
                    time.sleep(30)
                    continue
                break
            if weather['code'] == '404':
                continue

            # print(weather)
            for daily in weather["daily"]:
                temp_date_time = datetime.fromisoformat(daily["fxDate"])
                shanghai_timezone = pytz.timezone('Asia/Shanghai')
                date_time = temp_date_time.astimezone(shanghai_timezone)

                temp_aqi = random.randint(10, 150)  # TODO

                data = DailyWeather(
                    fxDate=date_time,
                    city=city_name,
                    adm2=adm2,
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
                
            if kwargs['print']:
                print('finish', city_name, adm2)
        self.stdout.write(self.style.SUCCESS('Successfully updated monthly weather info.'))
