from django.core.management.base import BaseCommand
from weather.models import LocationToInfo
import requests
import json
import time
import random

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
            "--no_key",
            action="store_true",
            help="randgen data",
        )

        parser.add_argument(
            "--stride",
            type=int,
            default=1,
            # help="Refresh All CityInfo even existed already",
        )

    def handle(self, *args, **kwargs):
        # LocationToInfo.objects.all().delete()
        # print("delete all")
        # print(len(LocationToInfo.objects.all()))
        # return
        if kwargs['D']:
            LocationToInfo.objects.all().delete()

        if kwargs["U"]:
            print("Refresh all")

        if kwargs["dev"]:
            url = 'https://devapi.qweather.com/v7/grid-weather/now'
        else:
            url = 'https://api.qweather.com/v7/grid-weather/now'

        stride = kwargs["stride"]
        for lon in range(73, 136, stride):
            for lat in range(3, 55, stride):

                location = "{:.2f},{:.2f}".format(lon, lat)


                if kwargs["no_key"]:
                    # print(location)
                    locationInfo = LocationToInfo(location=location, lon=lon, lat=lat)
                    # locationInfo.obsTime = Info["obsTime"]
                    locationInfo.temp = str(random.randint(0, 25))
                    locationInfo.aqi = str(random.randint(0, 100))
                    # locationInfo.icon = Info["icon"]
                    # locationInfo.text =  Info["text"]
                    locationInfo.wind360 = str(random.randint(0, 359))
                    di = ["西南风", "东北风"]
                    locationInfo.windDir = di[random.randint(0, 1)]
                    locationInfo.windScale = str(random.randint(1, 10))
                    locationInfo.windSpeed = str(random.randint(1, 10))
                    locationInfo.humidity = str(random.randint(1, 30))
                    locationInfo.precip = str(random.randint(1, 30))
                    locationInfo.pressure = str(random.randint(1, 100))
                    locationInfo.save()
                else:
                    try:
                        locationInfo = LocationToInfo.objects.get(location=location)
                        if not kwargs["U"] and locationInfo.obsTime != '':
                            continue
                    except:
                        locationInfo = LocationToInfo(location=location, lon=lon, lat=lat)

                    while True:
                        Info = requests.get(url, params={
                            'key': kwargs["key"],
                            'location': location,
                        })
                        Info = json.loads(Info.content.decode('utf-8'))
                        if Info["code"] == '429':
                            print("wait to access")
                            time.sleep(30)
                            continue
                        break


                    print(location, ":", Info)
                    if Info["code"] != '200':
                        print("Warning:", location, "get failed!", Info["code"])
                        print("check code on: https://dev.qweather.com/docs/resource/status-code/")
                        if Info["code"] != '402':
                            locationInfo.save()
                        else:
                            self.stdout.write(self.style.ERROR('Quata ran out!'))
                            return
                        continue

                    Info = Info["now"]

                    locationInfo.obsTime = Info["obsTime"]
                    locationInfo.temp = Info["temp"]
                    locationInfo.icon = Info["icon"]
                    locationInfo.text =  Info["text"]
                    locationInfo.wind360 = Info["wind360"]
                    locationInfo.windDir = Info["windDir"]
                    locationInfo.windScale = Info["windScale"]
                    locationInfo.windSpeed = Info["windSpeed"]
                    locationInfo.humidity = Info["humidity"]
                    locationInfo.precip = Info["precip"]
                    locationInfo.pressure = Info["pressure"]
                    locationInfo.save()


        print("DONE", len(LocationToInfo.objects.all()))
        for lat in range(54, 2, -1):
            for lon in range(73, 136, 1):
                location = "{:2f},{:2f}".format(lon, lat)
                try:
                    locationInfo = LocationToInfo.objects.get(location=location)
                except Exception as e:
                    print(location)
                    print(e)
                    self.stdout.write(self.style.ERROR('Incomplete!'))
                    return

                if locationInfo.obsTime == '':
                    print('.', end='')
                else:
                    print('#', end='')
            print("")


