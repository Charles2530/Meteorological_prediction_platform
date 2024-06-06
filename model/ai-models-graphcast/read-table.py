import csv
import math
from openpyxl import load_workbook

def calc(u, v):
    u = float(u)
    v = float(v)
    return str(math.sqrt(u * u + v * v))


f = open(r'/root/model/ai-models-graphcast/predictions.csv', 'r', newline='', encoding='utf-8')
reader = csv.reader(f)
cnt = 0
capital = dict()
for i, row in enumerate(reader):
    # if i < 2:
        # continue
    # if row[4] != '50' and row[4] != 'level':
        # continue
    for j, t in enumerate(row):
        print('({:d})'.format(j), t, end=' ')
    print('')
    if i > 10:
        break
    if row[4] != '50':
        continue
    flat = float(row[1])
    flon = float(row[2])


    if flat > 53.5 or flat < 3.5 or flon > 135 or flon < 73.5:
        continue

    time = row[0]
    lat = row[1]
    lon = row[2]



    windSpeed = calc(row[5], row[6])
    temp = str(float(row[7]) - 273.15)
    pressure = row[9]
    precip = row[12]
    # print(time, lat, lon, windSpeed, temp, pressure, precip)
    # print(i)
    # tim, lat, lon,
    # print(row[4])

