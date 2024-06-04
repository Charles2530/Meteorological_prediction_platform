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

    def handle(self, *args, **kwargs):
        if kwargs['D']:
            RealtimeWeather.objects.all().delete()

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

        count = kwargs['count']

        level_dict = {
            'Cancel': 1,
            'None': 1,
            'Unknown': 2,
            'Standard': 2,
            'Minor': 3,
            'Moderate': 3,
            'Major': 4,
            'Severe': 4
        }

        i = 0
        for location in warning_loc_list:
            if i > count:
                break
            location_id = location['locationId']
            warning_loc_response = requests.get(location_url, params={
                'key': kwargs['key'],
                'location': location_id,
            })
            warning_loc = json.loads(warning_loc_response.content.decode('utf-8'))['warning'].pop()

            weather_forecast = WeatherForecast(
                id=warning_loc['id'],
                img="https://ts1.cn.mm.bing.net/th/id/R-C.5b318dcf92724f1b99c194f891602f06?rik=eg7%2f2A2FtTorZA&riu=http%3a%2f%2fappdata.langya.cn%2fuploadfile%2f2020%2f0722%2f20200722090230374.jpg&ehk=DTXD%2bpXZoXFP8PBVpZeox9lN%2f5eoUhdebZg6f1gIPs0%3d&risl=&pid=ImgRaw&r=0",
                title=warning_loc['title'],
                # date=forecast['startTime'],
                city=warning_loc['sender'],
                level=level_dict.get(warning_loc['severity'], 5),
                content=warning_loc['text'],
                instruction="请有关单位和人员做好防范准备。"
            )
            weather_forecast.save()

            city = City2CityId.objects.get(cityId=location_id)
            location = city.location
            city_name = city.cityName

            hazard_info = HazardInfo(
                location=location,
                cityName=city_name,
                typeName=warning_loc['typeName'],
                time=datetime.fromisoformat(warning_loc['startTime']),
                # severity=warning_loc['severity'],
                severity=level_dict.get(warning_loc['severity'], 5),
                severityColor=warning_loc['severityColor'],
            )
            hazard_info.save()

            i += 1

        self.stdout.write(self.style.SUCCESS('Successfully updated catastrophic forecast data.'))



