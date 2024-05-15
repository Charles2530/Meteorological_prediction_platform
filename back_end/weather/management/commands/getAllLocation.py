from django.core.management.base import BaseCommand
from weather.models import LocationToInfo
import requests
import json
import time

class Command(BaseCommand):
    help = 'Store catastrophic forecast data into the database'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--U",
            action="store_true",
            help="Refresh All CityInfo even existed already",
        )

        parser.add_argument(
            "--key",
            default="feec92fecc5042f0b48e49c33529de89",
            help="Refresh All CityInfo even existed already",
        )

        parser.add_argument(
            "--dev",
            action="store_true",
            help="Refresh All CityInfo even existed already",
        )
        parser.add_argument(
            "--stride",
            type=int,
            default=1,
            # help="Refresh All CityInfo even existed already",
        )

    def handle(self, *args, **kwargs):
        if kwargs["U"]:
            print("refresh all")

        stride = kwargs["stride"]
        for lon in range(3, 55, stride):
            for lat in range(73, 136, stride):

                location = "{:d},{:d}".format(lon, lat)
                try:
                    locationInfo = LocationToInfo.objects.get(location=location)
                    if not kwargs["U"]:
                        continue
                except:
                    locationInfo = LocationToInfo(location=location, lon=lon, lat=lat)

                if kwargs["dev"]:
                    url = 'https://devapi.qweather.com/v7/grid-weather/now'
                else:
                    url = 'https://api.qweather.com/v7/grid-weather/now'
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


                print(Info)
                if Info["code"] != '200':
                    print("Warning:", location, "get failed!", Info["code"])
                    print("check code on: https://dev.qweather.com/docs/resource/status-code/")
                    if Info["code"] != '402':
                        locationInfo.save()
                    else:
                        self.stdout.write(self.style.ERROR('Quata ran out!'))
                        break
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




