from django.core.management.base import BaseCommand
import csv
from weather.models import City2CityId, Pro2City, ProGeography
from openpyxl import load_workbook

class Command(BaseCommand):
    help = 'Store catastrophic forecast data into the database'

    def handle(self, *args, **kwargs):
        f = open(r'/root/China-City-List-latest.csv', 'r', newline='', encoding='utf-8')
        reader = csv.reader(f)
        cnt = 0
        capital = dict()
        for i, row in enumerate(reader):
            if i < 2:
                continue
            if row[9].startswith(row[2]):
                cityId = row[0]
                cityName = row[9]
                capital.setdefault(row[7], row[0])
                Cityinfo = City2CityId(cityId=cityId, cityName=cityName)
                # try:
                Cityinfo.save()
                # except Exception as e:
                    # 1

        for pro, city in capital.items():
            Proinfo = Pro2City(proName=pro, cityId=city)
            Proinfo.save()


        workbook = load_workbook('/root/geography.xlsx')
        sheet = workbook.active

        # print(ProGeography.objects.filter())
        for row in sheet.iter_rows(values_only=True):
            geo = ProGeography(proName=row[0], geographyInfo=row[1])
            geo.save()
            # print(ProGeography.objects.get(proName=row[0]).proName)
            # print(row)
            # print(row[0], row[1])


