from datetime import datetime
import json
import requests
from django.core.management.base import BaseCommand, CommandParser
from notifications.models import WeatherForecast
from weather.models import RealtimeWeather, City2CityId, HazardInfo


class Command(BaseCommand):
    help = 'Store catastrophic forecast data into database'

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
            "--count",
            default=50,
            help="Specify count of warnings",
        )

        parser.add_argument(
            '--print',
            action='store_true',
            help='Print process',
        )

    def handle(self, *args, **kwargs):
        if kwargs['D']:
            print('Delete all')
            WeatherForecast.objects.all().delete()
            HazardInfo.objects.all().delete()

        if kwargs["U"]:
            print("Refresh all")

        if kwargs['dev']:
            warning_loc_list_url = 'https://devapi.qweather.com/v7/warning/list'
            location_url = 'https://devapi.qweather.com/v7/warning/now'
        else:
            warning_loc_list_url = 'https://api.qweather.com/v7/warning/list'
            location_url = 'https://api.qweather.com/v7/warning/now'

        # get city list
        warning_loc_list_response = requests.get(warning_loc_list_url, params={
            'key': kwargs['key'],
            'range': 'cn',
        })
        warning_loc_list = json.loads(warning_loc_list_response.content.decode('utf-8'))['warningLocList']

        count = int(kwargs['count'])

        level_dict = {
            'Cancel': 0,
            'None': 0,
            'Unknown': 0,
            'Standard': 1,
            'Minor': 2,
            'Moderate': 3,
            'Major': 4,
            'Severe': 5,
        }

        severity_dict = {
            'Cancel': '无',
            'None': '无',
            'Unknown': '未知',
            'Standard': '轻微',
            'Minor': '轻微',
            'Moderate': '中等',
            'Major': '较重',
            'Severe': '严重',
        }

        i = 0

        if kwargs['print']:
            print('get', count, 'items')

        for location in warning_loc_list:
            if i > count:
                break
            location_id = location['locationId']

            try:
                city = City2CityId.objects.get(cityId=location_id)
                city_name = city.cityName
                adm2 = city.areaName
                location = city.location
            except City2CityId.DoesNotExist:
                print('cannot get', location_id + '\'s warnings')
                continue

            if WeatherForecast.objects.filter(city=city_name, adm2=adm2).exists():
                print(city_name, adm2, 'already exists')
                continue

            while True:
                warning_loc_response = requests.get(location_url, params={
                    'key': kwargs['key'],
                    'location': location_id,
                })
                warning_loc_response = json.loads(warning_loc_response.content.decode('utf-8'))
                if warning_loc_response['code'] == '429':
                    print("wait to access")
                    time.sleep(30)
                    continue
                break

            if warning_loc_response['code'] == '404':
                continue

            warning_loc = warning_loc_response['warning'].pop()

            weather_forecast = WeatherForecast(
                id=warning_loc['id'],
                img="https://ts1.cn.mm.bing.net/th/id/R-C.5b318dcf92724f1b99c194f891602f06?rik=eg7%2f2A2FtTorZA&riu=http%3a%2f%2fappdata.langya.cn%2fuploadfile%2f2020%2f0722%2f20200722090230374.jpg&ehk=DTXD%2bpXZoXFP8PBVpZeox9lN%2f5eoUhdebZg6f1gIPs0%3d&risl=&pid=ImgRaw&r=0",
                title=warning_loc['title'],
                # date=forecast['startTime'],
                city=city_name,
                adm2=adm2,
                level=level_dict.get(warning_loc['severity'], 5),
                content=warning_loc['text'],
                instruction="请有关单位和人员做好防范准备。"
            )
            weather_forecast.save()

            hazard_info = HazardInfo(
                location=location,
                cityName=city_name,
                adm2=adm2,
                typeName=warning_loc['typeName'],
                time=datetime.fromisoformat(warning_loc['startTime']),
                severity=severity_dict.get(warning_loc['severity'], '未知'),
                severityColor=warning_loc['severityColor'],
            )
            hazard_info.save()

            i += 1

            if kwargs['print']:
                print('finish', city_name, adm2)

        self.stdout.write(self.style.SUCCESS('Successfully updated catastrophic forecast data.'))
