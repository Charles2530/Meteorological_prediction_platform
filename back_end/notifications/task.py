import requests
from celery import shared_task


@shared_task
def fetch_weather_catastrophic_forecast(location):
    url = 'https://devapi.qweather.com/v7/warning/now'
    params = {
        'key': 'f1aeb78d689f43bcafbba151a030019c',
        'location': location,
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data


@shared_task
def fetch_catastrophic_forecast_cities_list():
    url = 'https://devapi.qweather.com/v7/warning/list'
    params = {
        'key': 'aa7975af7b564c60804b6b08fab2e2c5',
        'range': 'cn',
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data
