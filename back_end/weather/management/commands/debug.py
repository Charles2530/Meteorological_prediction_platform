from django.core.management.base import BaseCommand
from weather.models import City2CityId, LocationToInfo
import requests
import json
import time

class Command(BaseCommand):
    help = 'Store catastrophic forecast data into the database'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--D',
            help='Delete all items in database',
        )

        parser.add_argument(
            "--U",
            action="store_true",
            help="Refresh All CityInfo even existed already",
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
            "--stride",
            type=int,
            default=1,
            # help="Refresh All CityInfo even existed already",
        )

    def handle(self, *args, **kwargs):
        tmp = LocationToInfo.objects.all()
        # print(tmp)
        # exit()
        # tt = City2CityId.objects.filter(cityName='北京市')
#

            # print(it.location, it.cityId, it.cityName, it.areaName)
            print(it.location, it.lon)

        # location_info = LocationToInfo.objects.get(location='95, 35')
        # print(tmp)



