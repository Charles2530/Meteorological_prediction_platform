from django.core.management.base import BaseCommand, CommandParser
from weather.models import WeatherInfo, City2CityId
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

        parser.add_argument(
            '--precise',
            action='store_true',
            help='Specify accuracy more precisely',
        )

    def handle(self, *args, **kwargs):
        if kwargs['D']:
            print('Delete all')
            WeatherInfo.objects.all().delete()

        if kwargs['dev']:
            historic_url = ''
            url = 'https://devapi.qweather.com/v7/weather/168h'
        else:
            historic_url = 'https://api.qweather.com/v7/historical/weather'
            url = 'https://api.qweather.com/v7/weather/168h'

        shanghai_timezone = pytz.timezone('Asia/Shanghai')

        if WeatherInfo.objects.count() > 0:
            # delete incomplete data
            city_name = WeatherInfo.objects.last().cityName
            adm2 = WeatherInfo.objects.last().adm2
            WeatherInfo.objects.filter(cityName=city_name, adm2=adm2).delete()

        for city in City2CityId.objects.all():
            location_id = city.cityId
            city_name = city.cityName
            adm2 = city.areaName

            if not kwargs['precise']:
                if WeatherInfo.objects.filter(cityName=city_name, adm2=adm2).exists():
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

                    for hourly in historic_weather["weatherHourly"]:
                        temp_date_time = datetime.fromisoformat(hourly['time']).astimezone(shanghai_timezone)
                        date_time = temp_date_time.astimezone(shanghai_timezone)

                        temp_aqi = random.randint(10, 150)  # TODO

                        if kwargs['precise']:
                            if WeatherInfo.objects.filter(time=date_time, cityName=city_name, adm2=adm2).exists():
                                continue

                        data = WeatherInfo(
                            time=date_time,
                            cityName=city_name,
                            adm2=adm2,
                            temp=hourly["temp"],
                            icon=hourly['icon'],
                            text=hourly["text"],
                            wind360=hourly["wind360"],
                            windDir=hourly["windDir"],
                            windScale=hourly["windScale"],
                            windSpeed=hourly["windSpeed"],
                            humidity=hourly["humidity"],
                            pressure=hourly["pressure"],
                            aqi=temp_aqi,
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
            for hourly in weather["hourly"]:
                dt = datetime.fromisoformat(hourly["fxTime"]).astimezone(shanghai_timezone)
                rounded_dt = dt.replace(minute=0, second=0, microsecond=0)

                temp_aqi = 28 + random.uniform(-10, 40)

                if kwargs['precise']:
                    if WeatherInfo.objects.filter(time=date_time, cityName=city_name, adm2=adm2).exists():
                        continue

                data = WeatherInfo(
                    time=rounded_dt,
                    cityName=city_name,
                    adm2=adm2,
                    temp=hourly["temp"],
                    icon=hourly['icon'],
                    text=hourly["text"],
                    wind360=hourly["wind360"],
                    windDir=hourly["windDir"],
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

            if kwargs['print']:
                print('finish', city_name, adm2)
            # city_name = ''
        self.stdout.write(self.style.SUCCESS('Successfully updated weather info.'))
