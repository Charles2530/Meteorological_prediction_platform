from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import HourlyWeather, DailyWeather, MonthlyWeather, Pro2City, ProGeography, City2CityId
from django.views.decorators.csrf import csrf_exempt
from .serializers import HourlyWeatherSerializer, DailyWeatherSerializer, MonthlyWeatherSerializer
import json
from datetime import datetime
import pytz


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


@csrf_exempt
def getProInfo(request):
    assert request.method == 'GET'
    proName = request.GET.get('proName')
    cityId = Pro2City.objects.get(proName=proName).cityId
    ### TODO use API to get weather and hazardTable
    # weather : 实时天气 https://dev.qweather.com/docs/api/weather/weather-now/
    # indices : 天气指数 https://dev.qweather.com/docs/resource/indices-info/
    # harzard :
    # json to dict TODO fill load paras
    weather = json.load(...)
    indices = json.load(...)
    hazrdTable = json.load(...)
    geography = ProGeography.objects.get(proName=proName).geographyInfo

    # retList = dict()
    # retList["weather"] = dict()
    # retList["geography"] = geography
    # retList["hazrdTable"] = dict()


    date_time = datetime.fromisoformat(weather["updateTime"])
    timezon = pytz.timezone('Asia/Shanghai')
    retList = {
        "weather": {
            "time": date_time.astimezone(timezon).strftime("%Y-%m-%d %H:%M"),
            "tem": ... ,
            "condition": ... ,
            "infos": ... ,
            "wind": ... ,
            "windDir": ... ,
            "hum": ... ,
            "ray": ... ,
            "air": ... ,
            "airAQI": ... ,
            "visibility": ... ,
            "rainfall": ... ,
            "pressure": ... ,
        },
        "geography": geography,
        "hazardTable": [
            {
                "place": ... ,
                "level": ... ,
                "type": ... ,
            },
            ...
        ]
    }

    return JsonResponse(retList, status=200)

@csrf_exempt
def getHazard(request: HttpRequest):
    assert request.method == 'GET'


@csrf_exempt
def getCityInfo(request: HttpRequest):
    assert request.method == 'GET'

    city = request.GET.get("city")
    cityId = City2CityId.objects.get(cityName=city)
    ### TODO use API to get weather and air
    # weather : 实时天气 https://dev.qweather.com/docs/api/weather/weather-now/
    # air : 实时空气质量 https://dev.qweather.com/docs/resource/indices-info/
    # json to dict TODO fill load paras
    weather = json.load(...)
    air = json.load(...)


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
            "windScale": float(weather["now"]["windScale"]),
            "windSpeed": float(weather["now"]["windSpeed"]),
            "humidity": float(weather["now"]["humidity"]),
            "pressure": float(weather["now"]["pressure"]),
            "aqi": float(air["now"]["aqi"]),
            "category": air["now"]["category"],
        },
    }
    return JsonResponse(retList, status=200)









