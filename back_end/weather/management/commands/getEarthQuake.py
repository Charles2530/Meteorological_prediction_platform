from django.core.management.base import BaseCommand
import csv
from weather.models import EarthQuakeInfo, LocationToInfo
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
        1

    # EarthQuakeInfo.objects.all().delete()
    # exit()
    def handle(self, *args, **kwargs):
        url = 'https://news.ceic.ac.cn/index.html'

        response = requests.get(url)
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')

        ls = soup.find_all('td', {'align': 'center'})

        # print(LocationToInfo.objects.all())

        for idx, it in enumerate(ls):
            if 'style' not in ls[idx].attrs or ls[idx]['style'] != 'padding-left: 20px':
                continue
            level = ls[idx].text
            time = ls[idx + 1].text
            lat = ls[idx + 2].text
            lon = ls[idx + 3].text
            depth = ls[idx + 4].text
            key = time + ' ' + lat + ' ' + lon
            # print(int(float(lat)), int(float(lon)))
            info = EarthQuakeInfo(level=level, time=time, lat=lat, lon=lon, depth=depth, key=key)
            info.save()

        print(len(EarthQuakeInfo.objects.all()))
