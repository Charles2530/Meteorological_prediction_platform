import requests
import gzip
import json
from celery import shared_task
from .models import Notification, WeatherForecast, CitySubscription
import json
import gzip


@shared_task
def fetch_weather_catastrophic_forecast(location):
    url = 'https://devapi.qweather.com/v7/warning/now'
    params = {
        'key': 'f1aeb78d689f43bcafbba151a030019c',
        'location': location,
    }
    response = requests.get(url, params=params)
    decompressed_data = gzip.decompress(response.content)
    data = json.loads(decompressed_data.decode('utf-8'))
    return data


@shared_task
def fetch_catastrophic_forecast_cities_list():
    url = 'https://devapi.qweather.com/v7/warning/list'
    params = {
        'key': 'aa7975af7b564c60804b6b08fab2e2c5',
        'range': 'cn',
    }
    response = requests.get(url, params=params)
    decompressed_data = gzip.decompress(response.content)
    data = json.loads(decompressed_data.decode('utf-8'))
    return data


def getLevel(severity):
    if severity == 'Cancel' or severity == 'None':
        return 1
    elif severity == 'Unknown' or severity == 'Standard':
        return 2
    elif severity == 'Minor' or severity == 'Moderate':
        return 3
    elif severity == 'Major' or severity == 'Severe':
        return 4
    else:
        return 5


def store_catastrophic_forecast_data():
    cities = fetch_catastrophic_forecast_cities_list()
    locations = cities['warningLocList']
    for locationId in locations:
        forecast = fetch_weather_catastrophic_forecast(location=locationId)
        forecast = forecast["warning"]
        weatherForecast = WeatherForecast(
            id=forecast['id'],
            img="https://ts1.cn.mm.bing.net/th/id/R-C.5b318dcf92724f1b99c194f891602f06?rik=eg7%2f2A2FtTorZA&riu=http%3a%2f%2fappdata.langya.cn%2fuploadfile%2f2020%2f0722%2f20200722090230374.jpg&ehk=DTXD%2bpXZoXFP8PBVpZeox9lN%2f5eoUhdebZg6f1gIPs0%3d&risl=&pid=ImgRaw&r=0",
            title=forecast['title'],
            date=forecast['startTime'],
            city=forecast['sender'],
            level=getLevel(forecast['severity']),
            content=forecast['text'],
            instruction="请有关单位和人员做好防范准备。"
        )
        weatherForecast.save()

# store_catastrophic_forecast_data()
