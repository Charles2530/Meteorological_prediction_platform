from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import HourlyWeather, DailyWeather, MonthlyWeather, Pro2City, ProGeography, City2CityId, WeatherInfo
from django.views.decorators.csrf import csrf_exempt
from .serializers import HourlyWeatherSerializer, DailyWeatherSerializer, MonthlyWeatherSerializer
import json
from datetime import datetime, timedelta
import pytz
import csv
import requests
import random

pri_key = "d4c9c9bc145748e48405c44277be0745"

# Create your views here.
class HourlyWeatherView(APIView):
    def get(self, request, format=None):
        hourly_weather = HourlyWeather.objects.all()
        serializer = HourlyWeatherSerializer(hourly_weather, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = HourlyWeatherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DailyWeatherView(APIView):
    def get(self, request, format=None):
        daily_weather = DailyWeather.objects.all()
        serializer = DailyWeatherSerializer(daily_weather, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DailyWeatherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MonthlyWeatherView(APIView):
    def get(self, request, format=None):
        monthly_weather = MonthlyWeather.objects.all()
        serializer = MonthlyWeatherSerializer(monthly_weather, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MonthlyWeatherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


def index(request):
    return HttpResponse("Welcome to the weather app!")


@require_http_methods(['GET'])
def overview(request):
    # query daily weather data
    weather = requests.get('https://devapi.qweather.com/v7/weather/now', params={
        'key': '7ddb2459227b4d6993afff0b4ba574ff',
        'location': '101010100',
    })

    weather = json.loads(weather.content.decode('utf-8'))
    data = weather['now']
    response_json = {
        "weather": {
            "condition": data.get("text", "Unknown"),  # 天气状况
            "temp": int(data.get("temp", 0)),  # 温度
            "temp_feel": int(data.get("temp", 0)),  # 体感温度
            "precip": float(data.get("precip", 0)),  # 降水量
            "precip_probability": 10,
            "aqi": 63,
            "pressure": int(data.get("pressure", 0)),  # 气压
            "ray": "中等",
            "sunrise_time": "5:04",
            "sunset_time": "19:19"
        },
        "search": True
    }
    
    # 返回转换后的JSON响应
    return JsonResponse(response_json, status=200)


def thirty_days_forecast(request):
    return HttpResponse("This is the 30 days forecast page!")


@require_http_methods(['GET'])
def realtime(request):
    # query realtime weather data
    current_time = datetime.now()
    url = 'https://devapi.qweather.com/v7/weather/now'
    params = {
        'key': 'f1aeb78d689f43bcafbba151a030019c',
        'location': '101010100', #TODO change to current cityId
    }
    response = requests.get(url, params=params)
    data = json.loads(response.content.decode('utf-8'))


    realTimeWeatherList = []
    current_index = int(data["updateTime"][11:13])  # Get the current hour
    for i in range(current_index-5, current_index+6):
        hour_index = i if i >= 0 else 24 + i  # Handle negative values
        hourly_data = data["hourly"][hour_index]
        realTimeWeatherList.append({
            "time": hourly_data["fxTime"][11:16],  # Extract hour and minute
            "condition": hourly_data["text"],
            "temperature": int(hourly_data["temp"]),
            "humidity": int(hourly_data["humidity"]),
            "windSpeed": int(hourly_data["windSpeed"]),
            "windDirection": hourly_data["windDir"]
        })

    return JsonResponse({"realTimeWeatherList": realTimeWeatherList})


@require_http_methods(['GET'])
def aqi_best(request):
    length = min(10, len(WeatherInfo.objects.all()))
    top_weather_info = WeatherInfo.objects.all().order_by('aqi')[:length]
    response_json = {
        "status": True,
        "ranks": [
            {
                "city": info.city,
                "category": info.category,
                "aqi": info.aqi
            }
            for info in top_weather_info
        ]
    }
    return JsonResponse(response_json, status=200)


@require_http_methods(['GET'])
def aqi_worst(request):
    length = min(10, len(WeatherInfo.objects.all()))
    lowest_weather_info = WeatherInfo.objects.all().order_by('-aqi')[:length]
    response_json = {
        "status": True,
        "ranks": [
            {
                "city": info.city,
                "category": info.category,
                "aqi": info.aqi
            }
            for info in lowest_weather_info
        ]
    }
    return JsonResponse(response_json, status=200)


@require_http_methods(['GET'])
def aqi_current_city_change(request):
    length = min(30, len(DailyWeather.objects.all()))
    all_info = DailyWeather.objects.filter(city='北京市').order_by('-fxDate')[:length]
    response_json = {
        "status": True,
        "data": [
            {
                "time": info.fxDate,
                "aqi": info.aqi,
            }
            for info in all_info
        ]
    }
    return JsonResponse(response_json, status=200)


def aqi_target_city_change(request):
    data = json.load(request.body)
    city = data["city"]
    length = min(30, len(DailyWeather.objects.all()))
    all_info = DailyWeather.objects.filter(city=city).order_by('-fxDate')[:length]
    response_json = {
        "status": True,
        "data": [
            {
                "time": info.fxDate,
                "aqi": info.aqi,
            }
            for info in all_info
        ]
    }
    return JsonResponse(response_json, status=200)


def temp_city_change(request):
    length = min(30, len(DailyWeather.objects.all()))
    all_info = DailyWeather.objects.filter(city='北京市').order_by('-fxDate')[:length]
    response_json = {
        "status": True,
        "data": [
            {
                "time": info.fxDate,
                "temp": info.tempMax,
            }
            for info in all_info
        ]
    }
    return JsonResponse(response_json, status=200)


def pressure_city_change(request):
    length = min(30, len(DailyWeather.objects.all()))
    all_info = DailyWeather.objects.filter(city='北京市').order_by('-fxDate')[:length]
    response_json = {
        "status": True,
        "data": [
            {
                "time": info.fxDate,
                "pressure": info.pressure,
            }
            for info in all_info
        ]
    }
    return JsonResponse(response_json, status=200)


def humid_city_change(request):
    length = min(30, len(DailyWeather.objects.all()))
    all_info = DailyWeather.objects.filter(city='北京市').order_by('-fxDate')[:length]
    response_json = {
        "status": True,
        "data": [
            {
                "time": info.fxDate,
                "humid": info.humidity,
            }
            for info in all_info
        ]
    }
    return JsonResponse(response_json, status=200)


@csrf_exempt
def getProInfo(request):
    assert request.method == 'GET'
    proName = request.GET.get('proName')
    if proName == '中国':
        proName = '北京市'
    cityId = Pro2City.objects.get(proName=proName).cityId
    cityName = City2CityId.objects.get(cityId=cityId).cityName
    # cityName = proName
    # cityId = "101010100"
    # cityName = '北京市'
    # proName = "北京"


    retList = {
        "weather": {
            "time": "2024-04-10 17:33",
            "tem": "11",
            "condition": "阴",
            "infos": "今晚多云。明天晴，比今天热很多，空气一般。",
            "icoid": "151",
            "wind": "2级",
            "windDir": "西南风",
            "hum": "70%",
            "ray": "中等",
            "air": "良",
            "airAQI": "91",
            "visibility": "9km",
            "rainfall": "0.0mm",
            "pressure": "1006hPa"
        },
        "geography": "河南省地势西高东低、北坦南凹，北、西、南三面有太行山、伏牛山、桐柏山、大别山四大山脉呈半环形分布， 中部和东部为辽阔的黄淮海冲积平原，西南部为南阳盆地。境内有黄河、淮河、卫河、汉水四大水系。大地构造跨华北板块和扬子板块，地层发育齐全，土壤分布大致以秦岭—淮河一线为界，此线以北为暖温带地带性土壤,此线以南地带性土壤为黄棕壤。",
        "hazardTable": [
            {
            "place": "葫芦岛市，河南省",
            "level": "蓝",
            "type": "大风"
            },
            {
            "place": "松原市，河南省",
            "level": "黄",
            "type": "森林火险"
            }
        ]
    }
    return JsonResponse(retList, status=200)
    ## TODO tochange



    ### use API to get weather and hazardTable
    # weather : 实时天气 https://dev.qweather.com/docs/api/weather/weather-now/
    # air : 实时空气质量 https://dev.qweather.com/docs/api/air/air-now/
    # indices : 天气指数 https://dev.qweather.com/docs/resource/indices-info/
    ## 运动指数，紫外线指数
    # harzard : 天气灾害预警 https://dev.qweather.com/docs/api/warning/weather-warning/
    weather = requests.get('https://devapi.qweather.com/v7/weather/now', params={
        'key': pri_key,
        'location': cityId,
    })
    air = requests.get('https://devapi.qweather.com/v7/air/now', params={
        'key': pri_key,
        'location': cityId,
    })
    indices = requests.get('https://devapi.qweather.com/v7/indices/1d', params={
        'key': pri_key,
        'location': cityId,
        'type': "1,5",
    })
    hazard = requests.get('https://devapi.qweather.com/v7/warning/now', params={
        'key': pri_key,
        'location': cityId,
    })

    weather = json.loads(weather.content.decode('utf-8'))
    air = json.loads(air.content.decode('utf-8'))
    indices = json.loads(indices.content.decode('utf-8'))
    hazard  = json.loads(hazard.content.decode('utf-8'))
    geography = ProGeography.objects.get(proName=proName).geographyInfo
    # geography = "geographyInf"


    date_time = datetime.fromisoformat(weather["updateTime"])
    timezon = pytz.timezone('Asia/Shanghai')
    date_time = date_time.astimezone(timezon).strftime("%Y-%m-%d %H:%M")

    retList = {
        "weather": {
            "time": date_time,
            "tem": float(weather["now"]["temp"]) ,
            "condition": weather["now"]["text"] ,
            "icoid": weather["now"]["icon"],
            "infos": "", # fill later
            "wind": int(weather["now"]["windScale"]) ,
            "windDir": weather["now"]["windDir"] ,
            "hum": int(weather["now"]["humidity"]) ,
            "ray": "" , # fill later
            "air": air["now"]["category"] ,
            "airAQI": int(air["now"]["aqi"]) ,
            "visibility": int(weather["now"]["vis"]) ,
            "rainfall": float(weather["now"]["precip"]) ,
            "pressure": int(weather["now"]["pressure"]) ,
        },
        "geography": geography,
        "hazardTable": [],
    }


    for daily in indices["daily"]:
        if daily["type"] == "1": # 运动指数
            retList["weather"]["infos"] = daily["text"]
        if daily["type"] == "5": # 紫外线
            retList["weather"]["ray"] = daily["category"]

    for warning in hazard["warning"]:
        retList["hazardTable"].append({
            "place": cityName + ", " + proName ,
            "level": warning["severityColor"] ,
            "type": warning["typeName"],
        })
    return JsonResponse(retList, status=200)

# @csrf_exempt
# def getHazard(request: HttpRequest):
#     assert request.method == 'GET'


@csrf_exempt
def getCityInfo(request: HttpRequest):
    assert request.method == 'GET'

    city = request.GET.get("city")
    ### TODO to remove
    city = "北京市"
    cityId = City2CityId.objects.get(cityName=city).cityId
    ### use API to get weather and air
    # weather : 实时天气 https://dev.qweather.com/docs/api/weather/weather-now/
    # air : 实时空气质量 https://dev.qweather.com/docs/api/air/air-now/
    weather = requests.get('https://devapi.qweather.com/v7/weather/now', params={
        'key': pri_key,
        'location': cityId,
    })
    air = requests.get('https://devapi.qweather.com/v7/air/now', params={
        'key': pri_key,
        'location': cityId,
    })

    weather = json.loads(weather.content.decode('utf-8'))
    air = json.loads(air.content.decode('utf-8'))


    date_time = datetime.fromisoformat(weather["updateTime"])
    timezon = pytz.timezone('Asia/Shanghai')
    retList = {
        "status": True,
        "message": {
            "time": date_time.astimezone(timezon).strftime("%Y-%m-%d %H:%M"),
            "city": city,
            "temp": float(weather["now"]["temp"]),
            "text": weather["now"]["text"],
            "precip": float(weather["now"]["precip"]),
            "wind360": float(weather["now"]["wind360"]),
            "windScale": int(weather["now"]["windScale"]),
            "windSpeed": float(weather["now"]["windSpeed"]),
            "humidity": int(weather["now"]["humidity"]),
            "pressure": int(weather["now"]["pressure"]),
            "aqi": int(air["now"]["aqi"]),
            "category": air["now"]["category"],
        },
    }
    return JsonResponse(retList, status=200)


# path('manage/data/weather_add/', views.add_weather_data, name='add_weather'),
# path('manage/data/delete/', views.delete_weather_data, name='delete_weather'),
# path('manage/data/search/', views.search_weather_data, name='search_weather'),
# class WeatherInfo(models.Model):
#     time = models.DateTimeField(default=datetime.now, primary_key=True)
#     city = models.CharField(max_length=200, default="北京", primary_key=True)
#     temp = models.FloatField(default=0.0)
#     text = models.CharField(max_length=200, default="")
#     precip = models.FloatField(default=0.0)
#     wind360 = models.FloatField(default=0.0)
#     windScale = models.IntegerField(default=0)
#     windSpeed = models.FloatField(default=0.0)
#     humidity = models.FloatField(default=0.0)
#     pressure = models.FloatField(default=0.0)
#     aqi = models.IntegerField(default=0)
#     category = models.CharField(max_length=200, default="")
@csrf_exempt
def add_weather_data(request):
    response_json = {
        "status": True,
    }
    data = json.loads(request.body)
    weather_info = WeatherInfo(
        time=data['time'],
        city=data['city'],
        temp=data['temp'],
        text=data['text'],
        precip=data['precip'],
        wind360=data['wind360'],
        windScale=data['windScale'],
        windSpeed=data['windSpeed'],
        humidity=data['humidity'],
        pressure=data['pressure'],
        aqi=data['aqi'],
        category=data['category'],
    )
    weather_info.save()
    return JsonResponse(response_json, status=200)


@csrf_exempt
def delete_weather_data(request):
    response_json = {
        "status": True,
    }
    data = json.loads(request.body)
    WeatherInfo.objects.filter(time=data['time'], city=data['city']).delete()
    return JsonResponse(response_json, status=200)


@csrf_exempt
def search_weather_data(request):
    data = json.loads(request.body)
    data_type = data['type'] if data['type'] else 'weather'
    from_time = data['time'][0] if len(data['time']) > 0 else None
    to_time = data['time'][1] if len(data['time']) > 1 else None
    address = data['address'] if data['address'] else None

    if data_type == 'weather':
        from django.db.models import Q

        # 定义时间范围过滤条件
        time_filter = Q(time__range=(from_time, to_time)
                        ) if from_time and to_time else Q()

        # 定义城市包含过滤条件
        city_filter = Q(city__contains=address) if address else Q()

        # 执行查询
        weather_data = WeatherInfo.objects.filter(time_filter & city_filter)
        # weather_data = WeatherInfo.objects.filter(
        #     time__range=(from_time, to_time) if from_time and to_time else all,
        #     city__contains=address if address else all
        # )
        weather_data_list = []
        for data in weather_data:
            weather_data_list.append({
                'time': data.fxTime,
                'city': data.city,
                'temp': data.temp,
                'text': data.text,
                'precip': data.precip,
                'wind360': data.wind360,
                'windScale': data.windScale,
                'windSpeed': data.windSpeed,
                'humidity': data.humidity,
                'pressure': data.pressure,
                'aqi': data.aqi,
                'category': data.category,
            })

        response_json = {
            "Status": True,
            "weatherHourlyList": weather_data_list
        }
        return JsonResponse(response_json, status=200)
    else:
        response_json = {
            "Status": False,
            "message": "Invalid data type"
        }
        return JsonResponse(response_json, status=400)
