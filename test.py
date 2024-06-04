
from bs4 import BeautifulSoup
import csv
import json
from openpyxl import load_workbook

f = open(r'/root/Meteorological_prediction_platform/back_end/China-City-List-latest.csv', 'r', newline='', encoding='utf-8')

reader = csv.reader(f)
cnt = 0

res = []
print('[')
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
    print(r'  { label: "' + city_n_area + r'", value: "' + city_n_area + r'" },')
    # try:
    # Cityinfo.cityName = cityName
    # Cityinfo.areaName = row[2]
    # print(row[2])
    # Cityinfo.location = "{:.2f},{:.2f}".format(float(row[11]), float(row[12]))
    # Cityinfo.save()

print(']')
js_data = json.dumps(res)

