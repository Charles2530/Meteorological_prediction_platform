# weather_fetcher.py
from django_cron import CronJobBase
from .views import fetch_weather_data
from django.utils import timezone
import requests
from datetime import datetime
from .models import HourlyWeather, DailyWeather, MonthlyWeather
from .serializers import HourlyWeatherSerializer, DailyWeatherSerializer, MonthlyWeatherSerializer


def fetch_weather_and_save_to_database():
    fetch_hourly_weather_and_save_to_database();
    fetch_daily_weather_and_save_to_database();
    # fetch_monthly_weather_and_save_to_database();


def fetch_realtime_weather_and_save_to_database():
    # todo 默认为北京，需要根据前端的返回值进行更改
    now_url = 'https://devapi.qweather.com/v7/weather/now'
    now_params = {
        'key': 'HE2404232054111443',
        'location': '101010100',
    }
    now_response = requests.get(now_url, params=now_params)
    now_data = now_response.json()
    now_item = now_data['now']

    air_url = 'https://devapi.qweather.com/airquality/v1/now'
    air_params = {
        'key': 'HE2404232054111443',
        'location': '101010100',
    }
    air_response = requests.get(air_url, params=air_params)
    air_data = air_response.json()
    air_item = air_data['aqi']

    realtime_overall_weather = HourlyWeather(
        obsTime=datetime.strptime(now_item['obsTime'], '%Y-%m-%dT%H:%M%z'),
        # location=params['location'],
        temp=now_item['temp'],
        text=now_item['text'],
        windDir=now_item['windDir'],
        windScale=now_item['windScale'],
        humidity=now_item['humidity'],
        pop=now_item['pop'],
        pressure=now_item['pressure'],
        air=air_item['category'],
        airAQI=air_item['value'],
    )
    # serializer = HourlyWeatherSerializer(data=data)
    # if serializer.is_valid():
    #     serializer.save()
    # else:
    #     print(serializer.errors)


def fetch_hourly_weather_and_save_to_database():
    # todo 默认为北京，需要根据前端的返回值进行更改
    url = 'https://devapi.qweather.com/v7/weather/24h'
    params = {
        'key': 'HE2404232054111443',
        'location': '101010100',
    }
    response = requests.get(url, params=params)
    data = response.json()

    hourly_weather_list = []
    for item in data['hourly']:
        hourly_weather = HourlyWeather(
            fxTime=datetime.strptime(item['fxTime'], '%Y-%m-%dT%H:%M%z'),
            location=params['location'],
            temp=item['temp'],
            icon=item['icon'],
            text=item['text'],
            wind360=item['wind360'],
            windDir=item['windDir'],
            windScale=item['windScale'],
            windSpeed=item['windSpeed'],
            humidity=item['humidity'],
            pop=item['pop'],
            precip=item['precip'],
            pressure=item['pressure'],
            cloud=item['cloud'],
            dew=item['dew']
        )
    hourly_weather_list.append(hourly_weather)

    # 将数据存储到数据库中
    HourlyWeather.objects.bulk_create(hourly_weather_list)
    
    # serializer = HourlyWeatherSerializer(data=data)
    # if serializer.is_valid():
    #     serializer.save()
    # else:
    #     print(serializer.errors)


def fetch_daily_weather_and_save_to_database():
    # todo 默认为北京，需要根据前端的返回值进行更改
    url = 'https://devapi.qweather.com/v7/weather/30d' # 默认查询30天的天气预报
    params = {
        'key': 'HE2404232054111443',
        'location': '101010100',
    }
    response = requests.get(url, params=params)
    data = response.json()


    daily_weather_list = []
    for item in data['daily']:
        daily_weather = DailyWeather(
            fxDate=item['fxDate'],
            sunrise=item['sunrise'],
            sunset=item['sunset'],
            moonrise=item['moonrise'],
            moonset=item['moonset'],
            moonPhase=item['moonPhase'],
            moonPhaseIcon=item['moonPhaseIcon'],
            tempMax=item['tempMax'],
            tempMin=item['tempMin'],
            iconDay=item['iconDay'],
            textDay=item['textDay'],
            iconNight=item['iconNight'],
            textNight=item['textNight'],
            wind360Day=item['wind360Day'],
            windDirDay=item['windDirDay'],
            windScaleDay=item['windScaleDay'],
            windSpeedDay=item['windSpeedDay'],
            wind360Night=item['wind360Night'],
            windDirNight=item['windDirNight'],
            windScaleNight=item['windScaleNight'],
            windSpeedNight=item['windSpeedNight'],
            humidity=item['humidity'],
            precip=item['precip'],
            pressure=item['pressure'],
            vis=item['vis'],
            cloud=item['cloud'],
            uvIndex=item['uvIndex']
        )
    daily_weather_list.append(daily_weather)

    # 将数据存储到数据库中
    DailyWeather.objects.bulk_create(daily_weather_list)
    # serializer = DailyWeatherSerializer(data=data)
    # if serializer.is_valid():
    #     serializer.save()
    # else:
    #     print(serializer.errors)


def fetch_monthly_weather_and_save_to_database():
    # todo 默认为北京，需要根据前端的返回值进行更改
    url = 'https://devapi.qweather.com/v7/weather/hourly'
    params = {
        'key': 'your_api_key',  # 请替换为您的API密钥
        'location': 'your_location',  # 请替换为您希望获取天气的地点
    }
    response = requests.get(url, params=params)
    data = response.json()

    serializer = MonthlyWeatherSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)


class WeatherUpdateJob(CronJobBase):
    run_every_mins = 1440  # 每天运行一次

    def do(self):
        fetch_weather_data()
