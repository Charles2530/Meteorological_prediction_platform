
from bs4 import BeautifulSoup
import csv
from openpyxl import load_workbook

        # try:
        #     f = open(r'/root/Meteorological_prediction_platform/back_end/China-City-List-latest.csv', 'r', newline='', encoding='utf-8')
        # except FileNotFoundError:
        #     try:
        #         f = open(r'D:\\Programing\\SoftwareEngineering\\Meteorological_prediction_platform\\back_end\\China-City-List-latest.csv', 'r', newline='', encoding='utf-8')
        #     except FileNotFoundError:
        #         pass

f = open(r'/root/Meteorological_prediction_platform/back_end/China-City-List-latest.csv', 'r', newline='', encoding='utf-8')

reader = csv.reader(f)
cnt = 0

res = []

for i, row in enumerate(reader):
    if i < 2:
        continue
    # cityId = row[0]
    # cityName = row[9]

    city_n_area = row[9] + ' ' + row[2]
    res.append({
        "label": city_n_area,
        "value": city_n_area,
    })

    # try:
    # Cityinfo.cityName = cityName
    # Cityinfo.areaName = row[2]
    # print(row[2])
    # Cityinfo.location = "{:.2f},{:.2f}".format(float(row[11]), float(row[12]))
    # Cityinfo.save()

