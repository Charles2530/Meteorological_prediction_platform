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


def overview(request):
    return HttpResponse("This is the weather app overview page!")


def thirty_days_forecast(request):
    return HttpResponse("This is the 30 days forecast page!")


def realtime(request):
    return HttpResponse("This is the realtime weather page!")


def aqi_best(request):
    return HttpResponse("This is the AQI best stations page!")


def aqi_worst(request):
    return HttpResponse("This is the AQI worst stations page!")


def aqi_current_city_change(request):
    return HttpResponse("This is the AQI current city change page!")


def aqi_target_city_change(request):
    return HttpResponse("This is the AQI target city change page!")


def temp_city_change(request):
    return HttpResponse("This is the temp city change page!")


def pressure_city_change(request):
    return HttpResponse("This is the pressure city change page!")


def humid_city_change(request):
    return HttpResponse("This is the humid city change page!")


# @csrf_exempt
# def getProInfo(request):
#     assert request.method == 'GET'
#     proName = request.GET.get('proName')
#     cityId = Pro2City.objects.get(proName=proName).cityId
#     ### TODO get cityName
#     # cityName = getCityName(cityId)
#     cityName = proName

#     ### TODO use API to get weather and hazardTable
#     # weather : 实时天气 https://dev.qweather.com/docs/api/weather/weather-now/
#     # air : 实时空气质量 https://dev.qweather.com/docs/resource/indices-info/
#     # indices : 天气指数 https://dev.qweather.com/docs/resource/indices-info/
#     ## 运动指数，紫外线指数
#     # harzard : 天气灾害预警 https://dev.qweather.com/docs/api/warning/weather-warning/
#     # json to dict TODO fill load paras
#     weather = json.load(...)
#     air = json.load(...)
#     indices = json.load(...)
#     hazard  = json.load(...)
#     geography = ProGeography.objects.get(proName=proName).geographyInfo


#     date_time = datetime.fromisoformat(weather["updateTime"])
#     timezon = pytz.timezone('Asia/Shanghai')
#     retList = {
#         "weather": {
#             "time": date_time.astimezone(timezon).strftime("%Y-%m-%d %H:%M"),
#             "tem": float(weather["now"]["temp"]) ,
#             "condition": weather["now"]["text"] ,
#             "infos": "", # fill later
#             "wind": int(weather["now"]["windScale"]) ,
#             "windDir": weather["now"]["windDir"] ,
#             "hum": int(weather["now"]["humidity"]) ,
#             "ray": "" , # fill later
#             "air": air["now"]["category"] ,
#             "airAQI": int(air["now"]["aqi"]) ,
#             "visibility": int(weather["now"]["vis"]) ,
#             "rainfall": float(weather["now"]["precip"]) ,
#             "pressure": int(weather["now"]["pressure"]) ,
#         },
#         "geography": geography,
#         "hazardTable": [],
#     }

#     for daily in indices["daily"]:
#         if daily.type == "1": # 运动指数
#             retList["weather"]["infos"] = daily["text"]
#         if daily.type == "5": # 紫外线
#             retList["weather"]["ray"] = daily["category"]

#     for warning in hazard["warning"]:
#         retList["hazardTable"].append({
#             "place": cityName + ", " + proName ,
#             "level": warning["severityColor"] ,
#             "type": warning["typeName"],
#         })


#     return JsonResponse(retList, status=200)

# @csrf_exempt
# def getHazard(request: HttpRequest):
#     assert request.method == 'GET'


# @csrf_exempt
# def getCityInfo(request: HttpRequest):
#     assert request.method == 'GET'

#     city = request.GET.get("city")
#     cityId = City2CityId.objects.get(cityName=city)
#     ### TODO use API to get weather and air
#     # weather : 实时天气 https://dev.qweather.com/docs/api/weather/weather-now/
#     # air : 实时空气质量 https://dev.qweather.com/docs/resource/indices-info/
#     # json to dict TODO fill load paras
#     weather = json.load(...)
#     air = json.load(...)


#     date_time = datetime.fromisoformat(weather["updateTime"])
#     timezon = pytz.timezone('Asia/Shanghai')
#     retList = {
#         "status": True,
#         "message": {
#             "time": date_time.astimezone(timezon).strftime("%Y-%m-%d %H:%M"),
#             "city": city,
#             "temp": float(weather["now"]["temp"]),
#             "text": weather["now"]["text"],
#             "precip": float(weather["now"]["precip"]),
#             "wind360": float(weather["now"]["wind360"]),
#             "windScale": int(weather["now"]["windScale"]),
#             "windSpeed": float(weather["now"]["windSpeed"]),
#             "humidity": int(weather["now"]["humidity"]),
#             "pressure": int(weather["now"]["pressure"]),
#             "aqi": int(air["now"]["aqi"]),
#             "category": air["now"]["category"],
#         },
#     }
#     return JsonResponse(retList, status=200)









