from django.core.management.base import BaseCommand
import csv
from weather.models import EarthQuakeInfo
from openpyxl import load_workbook
import requests
from bs4 import BeautifulSoup

class Command(BaseCommand):
    def add_arguments(self, parser):
        # Named (optional) arguments
        # parser.add_argument(
            # "--U",
            # action="store_true",
            # help="Refresh All CityInfo even existed already",
        # )
        parser.add_argument(
            "--filter",
            action="store_true",
            help="Refresh All CityInfo even existed already",
        ) # no impl
        1

    # EarthQuakeInfo.objects.all().delete()
    # exit()
    def handle(self, *args, **kwargs):
        url = 'https://news.ceic.ac.cn/index.html'

        response = requests.get(url)
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')

        EarthQuakeInfo.objects.all().delete()
        ls = soup.find_all('tr')
        for it in ls:
            if it.children is None:
                continue
                # and it.children[0].name == 'td':
                # print(it.children[0].name)
            clist = [j for j in it.children]
            if len(clist) != 6 or clist[0].name != 'td':
                continue

            # if kwargs["filter"]:

                # continue
            level = clist[0].text
            time = clist[1].text
            lat = clist[2].text
            lon = clist[3].text
            depth = clist[4].text
            location = clist[5].text
            key = time + ' ' + lat + ' ' + lon
            if float(lat) > 53.5 or float(lat) < 3.5 or float(lon) > 135 or float(lon) < 73.5:
                continue
            print(float(lat), float(lon))
            info = EarthQuakeInfo(
                level=level, time=time, lat=lat, lon=lon,
                depth=depth, location=location, key=key
            )
            info.save()

        print(len(EarthQuakeInfo.objects.all()))
