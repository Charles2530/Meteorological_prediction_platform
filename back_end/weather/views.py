import csv
import json
import random
from datetime import date, datetime, timedelta

import pytz
import requests
from customuser.models import UserCurrentCity
from notifications.models import CitySubscription
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RealtimeWeather, RealtimeAirQuality
from .models import HourlyWeather, DailyWeather, MonthlyWeather, WeatherInfo
from .models import Pro2City, ProGeography, City2CityId, LocationToInfo
from .models import HazardInfo, EarthQuakeInfo
from .serializers import RealtimeWeatherSerializer, RealtimeAirQualitySerializer
from .serializers import HourlyWeatherSerializer, DailyWeatherSerializer, MonthlyWeatherSerializer, \
    WeatherInfoSerializer
from .serializers import Pro2CitySerializer, ProGeographySerializer, City2CityIdSerializer, LocationToInfoSerializer
from .serializers import HazardInfoSerializer, EarthQuakeInfoSerializer

pri_key = "d4c9c9bc145748e48405c44277be0745"


# Create your views here.
class RealtimeWeatherView(APIView):
    @staticmethod
    def get(request, format=None):
        realtime_weather = RealtimeWeather.objects.all()
        serializer = HourlyWeatherSerializer(realtime_weather, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, format=None):
        serializer = RealtimeWeatherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class RealtimeAirQualityView(APIView):
    @staticmethod
    def get(request, format=None):
        realtime_air_quality = RealtimeAirQuality.objects.all()
        serializer = RealtimeAirQualitySerializer(realtime_air_quality, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, format=None):
        serializer = RealtimeAirQualitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class HourlyWeatherView(APIView):
    @staticmethod
    def get(request, format=None):
        hourly_weather = HourlyWeather.objects.all()
        serializer = HourlyWeatherSerializer(hourly_weather, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, format=None):
        serializer = HourlyWeatherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DailyWeatherView(APIView):
    @staticmethod
    def get(request, format=None):
        daily_weather = DailyWeather.objects.all()
        serializer = DailyWeatherSerializer(daily_weather, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, format=None):
        serializer = DailyWeatherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MonthlyWeatherView(APIView):
    @staticmethod
    def get(request, format=None):
        monthly_weather = MonthlyWeather.objects.all()
        serializer = MonthlyWeatherSerializer(monthly_weather, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, format=None):
        serializer = MonthlyWeatherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class WeatherInfoView(APIView):
    @staticmethod
    def get(request, format=None):
        weather_info = WeatherInfo.objects.all()
        serializer = WeatherInfoSerializer(weather_info, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, format=None):
        serializer = WeatherInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class Pro2CityView(APIView):
    @staticmethod
    def get(request, format=None):
        pro2city_info = Pro2City.objects.all()
        serializer = Pro2CitySerializer(pro2city_info, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, format=None):
        serializer = Pro2CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ProGeographyView(APIView):
    @staticmethod
    def get(request, format=None):
        pro_geography_info = ProGeography.objects.all()
        serializer = ProGeographySerializer(pro_geography_info, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, format=None):
        serializer = ProGeographySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class City2CityIdView(APIView):
    @staticmethod
    def get(request, format=None):
        city2cityid_info = City2CityId.objects.all()
        serializer = City2CityIdSerializer(city2cityid_info, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, format=None):
        serializer = City2CityIdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LocationToInfoView(APIView):
    @staticmethod
    def get(request, format=None):
        location_to_info = LocationToInfo.objects.all()
        serializer = LocationToInfoSerializer(location_to_info, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, format=None):
        serializer = LocationToInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class HazardInfoView(APIView):
    @staticmethod
    def get(request, format=None):
        hazard_info = HazardInfo.objects.all()
        serializer = HazardInfoSerializer(hazard_info, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, format=None):
        serializer = HazardInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class EarthQuakeInfoView(APIView):
    @staticmethod
    def get(request, format=None):
        earthquake_info = EarthQuakeInfo.objects.all()
        serializer = EarthQuakeInfoSerializer(earthquake_info, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, format=None):
        serializer = EarthQuakeInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


def index(request):
    return HttpResponse("Welcome to the weather app!")


@require_http_methods(['GET'])
def overview(request):
    # query daily weather data
    city_name = request.GET.get('city[name]')
    adm2 = request.GET.get('city[adm2]')

    try:
        realtime_weather = RealtimeWeather.objects.get(cityName=city_name, adm2=adm2)
    except RealtimeWeather.DoesNotExist:
        realtime_weather = RealtimeWeather.objects.filter(cityName='北京市').first()
    try:
        daily_weather = DailyWeather.objects.filter(city=city_name, adm2=adm2, fxDate=date.today()).first()
    except DailyWeather.DoesNotExist:
        daily_weather = DailyWeather.objects.filter(city='北京市').first()
    try:
        realtime_air_quality = RealtimeAirQuality.objects.filter(cityName=city_name, adm2=adm2).first()
    except RealtimeAirQuality.DoesNotExist:
        realtime_air_quality = RealtimeAirQuality.objects.filter(cityName='北京市').first()
    response_json = {
        "weather": {
            "condition": realtime_weather.text if realtime_weather else 0,
            "condition_icon": realtime_weather.icon if realtime_weather else 0,
            "temp": realtime_weather.temp if realtime_weather else 0,
            "temp_feel": realtime_weather.feelsLike if realtime_weather else 0,
            "precip": realtime_weather.precip if realtime_weather else 0,
            "precip_probability": 10,  # TODO change with real data
            "aqi": realtime_air_quality.aqi if realtime_air_quality else 0,
            "pressure": realtime_weather.pressure if realtime_air_quality else 0,
            "ray": "中等",  # TODO change with real data
            "sunrise_time": daily_weather.sunrise if daily_weather else 0,
            "sunset_time": daily_weather.sunset if daily_weather else 0,
            "humidity": daily_weather.humidity if daily_weather else 0,
        },
        "search": True
    }

    return JsonResponse(response_json, status=200)


@require_http_methods(['GET'])
def realtime(request):
    # query realtime weather data
    # query hourly weather data
    city_name = request.GET.get('city[name]')
    adm2 = request.GET.get('city[adm2]')

    realTimeWeatherList = []
    rounded_dt = datetime.now().replace(minute=0, second=0, microsecond=0)
    fake_rounded_dt = rounded_dt + timedelta(days=1)  # use tomorrow data for query
    for i in range(-5, 7):
        query_dt = fake_rounded_dt + timedelta(hours=i)
        print_dt = rounded_dt + timedelta(hours=i)
        hourly_weather = WeatherInfo.objects.filter(cityName=city_name, adm2=adm2, time=query_dt).first()
        realTimeWeatherList.append({
            "time": print_dt.strftime('%I:%M'),
            "condition": hourly_weather.text if hourly_weather else 0,
            'condition_icon': hourly_weather.icon if hourly_weather else 0,
            "temperature": int(hourly_weather.temp if hourly_weather else 0),
            "humidity": int(hourly_weather.humidity if hourly_weather else 0),
            "windScale": int(hourly_weather.windScale.split('-')[-1] if hourly_weather else 0),
            "windDirection": hourly_weather.windDir if hourly_weather else 0,
            'wind360': hourly_weather.wind360 if hourly_weather else 0,
        })

    return JsonResponse({"realTimeWeatherList": realTimeWeatherList})


@require_http_methods(['GET'])
def city_rank(request):
    city_list_max_temp = []
    city_list_min_temp = []
    city_list_precip = []
    city_list_worst_aqi = []
    city_list_best_aqi = []

    length = min(10, len(RealtimeWeather.objects.all())) + 1
    top_weather_info = RealtimeWeather.objects.all().order_by('-temp')[:length]
    for i in range(length):
        info = top_weather_info[i]
        city_list_max_temp.append({
            'no': i + 1,
            "city": info.adm2,
            'province': info.cityName,
            "item": getattr(info, 'temp')
        })

    top_weather_info = RealtimeWeather.objects.all().order_by('temp')[:length]
    for i in range(length):
        info = top_weather_info[i]
        city_list_min_temp.append({
            'no': i + 1,
            "city": info.adm2,
            'province': info.cityName,
            "item": getattr(info, 'temp')
        })

    top_weather_info = RealtimeWeather.objects.all().order_by('-precip')[:length]
    for i in range(length):
        info = top_weather_info[i]
        city_list_precip.append({
            'no': i + 1,
            "city": info.adm2,
            'province': info.cityName,
            "item": getattr(info, 'precip')
        })

    length = min(10, len(RealtimeAirQuality.objects.all())) + 1
    top_weather_info = RealtimeAirQuality.objects.all().order_by('-aqi')[:length]
    for i in range(length):
        info = top_weather_info[i]
        city_list_worst_aqi.append({
            'no': i + 1,
            "city": info.adm2,
            'province': info.cityName,
            "item": getattr(info, 'aqi')
        })

    top_weather_info = RealtimeAirQuality.objects.all().order_by('aqi')[:length]
    for i in range(length):
        info = top_weather_info[i]
        city_list_best_aqi.append({
            'no': i + 1,
            "city": info.adm2,
            'province': info.cityName,
            "item": getattr(info, 'aqi')
        })

    json_response = {
        'city_list_max_temp': city_list_max_temp,
        'city_list_min_temp': city_list_min_temp,
        'city_list_precip': city_list_precip,
        'city_list_worst_aqi': city_list_worst_aqi,
        'city_list_best_aqi': city_list_best_aqi,
    }

    return JsonResponse(json_response, status=200)


@csrf_exempt
@login_required
@require_http_methods(['POST'])
def add_care_city(request):
    data = json.loads(request.body)

    city_name = data.get('city').get('name')
    adm2 = data.get('city').get('adm2')
    user = request.user
    if not city_name:
        return JsonResponse({'status': False, 'message': 'No cities provided.'}, status=400)
    # print('-----', user.username, cities, '-----')
    if CitySubscription.objects.filter(user=user, cityName=city_name, adm2=adm2).exists():
        CitySubscription.objects.filter(user=user, cityName=city_name, adm2=adm2).delete()
    else:
        city_subscription = CitySubscription(
            user=user,
            cityName=city_name,
            adm2=adm2
        )
        city_subscription.save()

    return JsonResponse({'status': True})


@csrf_exempt
@login_required
@require_http_methods(['POST'])
def delete_care_city(request):
    data = json.loads(request.body)

    city_name = data.get('city').get('name')
    adm2 = data.get('city').get('adm2')
    user = request.user
    if not city_name:
        return JsonResponse({'status': False, 'message': 'No cities provided.'}, status=400)
    # print('-----', user.username, cities, '-----')
    if CitySubscription.objects.filter(user=user, cityName=city_name, adm2=adm2).exists():
        CitySubscription.objects.filter(user=user, cityName=city_name, adm2=adm2).delete()
    else:
        city_subscription = CitySubscription(
            user=user,
            cityName=city_name,
            adm2=adm2
        )
        city_subscription.save()

    return JsonResponse({'status': True})


@require_http_methods(['GET'])
@login_required
def subscribed_cities_summary(request):
    user = request.user
    current_city = UserCurrentCity.objects.get(user=user)
    subscriptions = CitySubscription.objects.filter(user=user)
    # print('-----', current_city.cityName, '-----')
    if current_city.cityName.find(' ') != -1:
        current_city_name = current_city.cityName.split()[0]
        current_adm2 = current_city.cityName.split()[1]
    else:
        current_city_name = current_city.cityName
        current_adm2 = current_city.adm2
        if current_city.adm2 == '':
            current_adm2 = '海淀'  # TODO 区
        # elif current_city.adm2.find('区') == -1:
        #     current_adm2 += '区'
    # print('-----', 'current_city_name', current_city_name, '-----')
    # print('-----', 'current_adm2', current_adm2, '-----')
    care_cities_list = []
    for subscription in subscriptions:
        subscription_city_name = subscription.cityName
        subscription_adm2 = subscription.adm2
        if subscription_adm2 == '':
            current_adm2 = '海淀'  # TODO 区
        # elif subscription_adm2.find('区') == -1:
        #     current_adm2 += '区'
        realtime_weather = RealtimeWeather.objects.get(cityName=subscription_city_name, adm2=subscription_adm2)
        if realtime_weather is None:
            realtime_weather = RealtimeWeather.objects.first()
        care_cities_list.append({
            'city': {
                'name': subscription_city_name,
                'adm2': subscription_adm2,
            },
            'temp': realtime_weather.temp,
            'cond_icon': realtime_weather.icon,
        })
    json_response = {
        'success': True,
        'currentCity': {
            'city': {
                'name': current_city_name,
                'adm2': current_adm2,
            },
            'temp': RealtimeWeather.objects.get(cityName=current_city_name, adm2=current_adm2).temp,
            'cond_icon': RealtimeWeather.objects.get(cityName=current_city_name, adm2=current_adm2).icon,
        },
        'careCitiesList': care_cities_list,
    }
    return JsonResponse(json_response)


@require_http_methods(['GET'])
def aqi_detail(request):
    name = request.GET.get('city[name]')
    adm2 = request.GET.get('city[adm2]')

    aqi_info = RealtimeAirQuality.objects.filter(cityName='北京市', adm2='北京').first()
    response_json = {
        "aqi": float(aqi_info.aqi),
        "category": aqi_info.category,
        "pm10": float(aqi_info.pm10),
        "pm2.5": float(aqi_info.pm2p5),
        "no2": float(aqi_info.no2),
        "so2": float(aqi_info.so2),
        "co": float(aqi_info.co),
        "o3": float(aqi_info.o3),
    }
    return JsonResponse(response_json)


@require_http_methods(['GET'])
def rank(request):
    length = min(10, len(WeatherInfo.objects.all())) + 1
    norm = request.GET.get('norm')
    if norm == 'humid':
        norm = 'humidity'
    ascending = request.GET.get('order_type')
    if ascending == 'true':
        top_weather_info = WeatherInfo.objects.all().order_by('-' + norm)[:length]
    elif ascending == 'false':
        top_weather_info = WeatherInfo.objects.all().order_by(norm)[:length]
    response_json = {
        "status": True,
        "ranks": [
            {
                "city": info.cityName + ' ' + info.adm2,
                "level": "优" if ascending=="true" else "正常",
                "norm": getattr(info, norm)
            }
            for info in top_weather_info
        ]
    }
    return JsonResponse(response_json, status=200)


@require_http_methods(['GET'])
def aqi_current_city_change(request):
    length = min(30, len(DailyWeather.objects.all())) + 1
    all_info = DailyWeather.objects.filter(
        city='北京市').order_by('-fxDate')[:length]
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


@require_http_methods(['GET'])
def target_city_change(request, norm):
    city = request.GET.get('city')
    period = int(request.GET.get('periods'))
    length = min(period, len(DailyWeather.objects.all())) + 1
    all_info = DailyWeather.objects.filter(
        city=city).order_by('fxDate')[:length]
    response_json = {
        "status": True,
        "data": [
            {
                "time": info.fxDate,
                norm: info.norm,  # TODO
            }
            for info in all_info
        ]
    }
    return JsonResponse(response_json, status=200)


@require_http_methods(['GET'])
def aqi_target_city_change(request):
    city = request.GET.get('city')
    period = int(request.GET.get('periods'))
    length = min(period, len(DailyWeather.objects.all())) + 1
    all_info = DailyWeather.objects.filter(
        city=city.split(" ")[0],adm2=city.split(" ")[1]).order_by('fxDate')[:length]
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


@require_http_methods(['GET'])
def humid_city_change(request):
    city = request.GET.get('city')
    period = int(request.GET.get('periods'))
    length = min(period, len(DailyWeather.objects.all())) + 1
    all_info = DailyWeather.objects.filter(
        city=city.split(" ")[0],adm2=city.split(" ")[1]).order_by('fxDate')[:length]
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


def temp_city_change(request):
    city = request.GET.get('city')
    period = int(request.GET.get('periods'))
    length = min(period, len(DailyWeather.objects.all())) + 1
    all_info = DailyWeather.objects.filter(
        city=city.split(" ")[0],adm2=city.split(" ")[1]).order_by('fxDate')[:length]
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


def temp_city_change_detail(request):
    city = request.GET.get('city')
    period = int(request.GET.get('periods'))
    length = min(period, len(DailyWeather.objects.all())) + 1
    all_info = DailyWeather.objects.filter(
        city=city.split(" ")[0],adm2=city.split(" ")[1]).order_by('fxDate')[:length]
    response_json = {
        "status": True,
        "data": [
            {
                "time": info.fxDate,
                "temp": str((float(info.tempMax) + float(info.tempMin)) / 2),
                "maxTemp": info.tempMax,
                "minTemp": info.tempMin
            }
            for info in all_info
        ]
    }
    return JsonResponse(response_json, status=200)


@require_http_methods(['GET'])
def pressure_city_change(request):
    city = request.GET.get('city')
    period = int(request.GET.get('periods'))
    length = min(period, len(DailyWeather.objects.all())) + 1
    all_info = DailyWeather.objects.filter(
        city=city.split(" ")[0],adm2=city.split(" ")[1]).order_by('fxDate')[:length]
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


@require_http_methods(['GET'])
def precip_city_change(request):
    city = request.GET.get('city')
    period = int(request.GET.get('periods'))
    length = min(period, len(DailyWeather.objects.all())) + 1
    all_info = DailyWeather.objects.filter(
        city=city.split(" ")[0],adm2=city.split(" ")[1]).order_by('fxDate')[:length]
    response_json = {
        "status": True,
        "data": [
            {
                "time": info.fxDate,
                "precip": info.precip,
            }
            for info in all_info
        ]
    }
    return JsonResponse(response_json, status=200)


@require_http_methods(['GET'])
def winspeed_city_change(request):
    city = request.GET.get('city')
    period = int(request.GET.get('periods'))
    length = min(period, len(DailyWeather.objects.all())) + 1
    all_info = DailyWeather.objects.filter(
        city=city.split(" ")[0],adm2=city.split(" ")[1]).order_by('fxDate')[:length]
    response_json = {
        "status": True,
        "data": [
            {
                "time": info.fxDate,
                "winSpeed": info.windSpeedDay,
            }
            for info in all_info
        ]
    }
    return JsonResponse(response_json, status=200)


@require_http_methods(['GET'])
def getProInfo(request):
    proName = request.GET.get('proName')
    if proName == '中国':
        proName = '北京市'
    cityId = Pro2City.objects.get(proName=proName).cityId
    cityName = City2CityId.objects.get(cityId=cityId).cityName
    # cityName = proName
    # cityId = "101010100"
    # cityName = '北京市'
    # proName = "北京"

    # retList = {
    #     "weather": {
    #         "time": "2024-04-10 17:33",
    #         "tem": "11",
    #         "condition": "阴",
    #         "infos": "今晚多云。明天晴，比今天热很多，空气一般。",
    #         "icoid": "151",
    #         "wind": "2级",
    #         "windDir": "西南风",
    #         "hum": "70%",
    #         "ray": "中等",
    #         "air": "良",
    #         "airAQI": "91",
    #         "visibility": "9km",
    #         "rainfall": "0.0mm",
    #         "pressure": "1006hPa"
    #     },
    #     "geography": "河南省地势西高东低、北坦南凹，北、西、南三面有太行山、伏牛山、桐柏山、大别山四大山脉呈半环形分布， 中部和东部为辽阔的黄淮海冲积平原，西南部为南阳盆地。境内有黄河、淮河、卫河、汉水四大水系。大地构造跨华北板块和扬子板块，地层发育齐全，土壤分布大致以秦岭—淮河一线为界，此线以北为暖温带地带性土壤,此线以南地带性土壤为黄棕壤。",
    #     "hazardTable": [
    #         {
    #         "place": "葫芦岛市，河南省",
    #         "level": "蓝",
    #         "type": "大风"
    #         },
    #         {
    #         "place": "松原市，河南省",
    #         "level": "黄",
    #         "type": "森林火险"
    #         }
    #     ]
    # }
    # return JsonResponse(retList, status=200)
    # TODO tochange

    # use API to get weather and hazardTable
    # weather : 实时天气 https://dev.qweather.com/docs/api/weather/weather-now/
    # air : 实时空气质量 https://dev.qweather.com/docs/api/air/air-now/
    # indices : 天气指数 https://dev.qweather.com/docs/resource/indices-info/
    # 运动指数，紫外线指数
    # hazard : 天气灾害预警 https://dev.qweather.com/docs/api/warning/weather-warning/
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
    hazard = json.loads(hazard.content.decode('utf-8'))
    geography = ProGeography.objects.get(proName=proName).geographyInfo
    # geography = "geographyInf"

    date_time = datetime.fromisoformat(weather["updateTime"])
    timezon = pytz.timezone('Asia/Shanghai')
    date_time = date_time.astimezone(timezon).strftime("%Y-%m-%d %H:%M")

    retList = {
        "weather": {
            "time": date_time,
            "tem": float(weather["now"]["temp"]),
            "condition": weather["now"]["text"],
            "icoid": weather["now"]["icon"],
            "infos": "",  # fill later
            "wind": int(weather["now"]["windScale"]),
            "windDir": weather["now"]["windDir"],
            "hum": int(weather["now"]["humidity"]),
            "ray": "",  # fill later
            "air": air["now"]["category"],
            "airAQI": int(air["now"]["aqi"]),
            "visibility": int(weather["now"]["vis"]),
            "rainfall": float(weather["now"]["precip"]),
            "pressure": int(weather["now"]["pressure"]),
        },
        "geography": geography,
        "hazardTable": [
            {

            }
        ],
    }

    for daily in indices["daily"]:
        if daily["type"] == "1":  # 运动指数
            retList["weather"]["infos"] = daily["text"]
        if daily["type"] == "5":  # 紫外线
            retList["weather"]["ray"] = daily["category"]

    for warning in hazard["warning"]:
        retList["hazardTable"].append({
            "place": cityName + ", " + proName,
            "level": warning["severityColor"],
            "type": warning["typeName"],
        })
    return JsonResponse(retList, status=200)


@csrf_exempt
@login_required
@require_http_methods(['POST'])
def update_current_city(request):
    user = request.user
    city = request.POST.get('city')
    if city:
        user.currentCityName = city
        user.save()
        return JsonResponse({
            "success": True,
            "reason": ""
        })
    else:
        return JsonResponse({
            "success": False,
            "reason": "city doesn't exist"
        })


@require_http_methods(['GET'])
def get_hazard(request: HttpRequest):
    all_info = HazardInfo.objects.all()
    response_json = [
        {
            "place": info.cityName,
            "longitude": City2CityId.objects.filter(cityName=info.cityName).first().location.split(',')[1].strip(),
            "latitude": City2CityId.objects.filter(cityName=info.cityName).first().location.split(',')[0].strip(),
            "type": info.typeName,
            "time": '',  # TODO fix date str time
            "level": info.severity,
        }
        for info in all_info
    ]

    eq_info = EarthQuakeInfo.objects.all()
    response_json.extend([{
        "place": info.location,
        "longitude": info.lon,
        "latitude": info.lat,
        "type": "地震",
        "time": info.time,  # TODO fix date str time
        "level": info.level,
    } for info in eq_info])

    return JsonResponse({"data": response_json}, status=200)


@csrf_exempt
@require_http_methods(['GET'])
def get_top_hazard(request: HttpRequest):
    all_info = HazardInfo.objects.filter(severity='Severe' or 'Extreme').order_by('-time')
    response_json = [
        {
            "place": info.cityName,
            "longitude": City2CityId.objects.filter(cityName=info.cityName).first().location.split(',')[1].strip(),
            "latitude": City2CityId.objects.filter(cityName=info.cityName).first().location.split(',')[0].strip(),
            "type": info.typeName,
            "time": '',  # TODO fix date str time
            "level": info.severity,
        }
        for info in all_info
    ]

    eq_info = EarthQuakeInfo.objects.all()
    for info in eq_info:
        if float(str(info.level)) > 5.0:
            response_json.append({
                "place": info.location,
                "longitude": info.lon,
                "latitude": info.lat,
                "type": "地震",
                "time": info.time,  # TODO fix date str time
                "level": info.level,
            })

    return JsonResponse({'data': response_json}, status=200)


@csrf_exempt
@require_http_methods(['GET'])
def get_city_info(request: HttpRequest):
    city = request.GET.get("city")
    shanghai_timezone = pytz.timezone('Asia/Shanghai')
    if city=="":
        retList = {
            "status": True,
            "message": {
                "time": datetime.now(shanghai_timezone).strftime("%Y-%m-%d %H:%M"),
                "city": "北京市 北京",
                "temp": "晴",
                "text": 0,
                "precip": 0,
                "wind360": 0,
                "windScale": 0,
                "windSpeed": 0,
                "humidity": 0,
                "pressure": 0,
                "aqi": 0,
                "category": "优",
            },
        }
        return JsonResponse(retList, status=204)
    city_name = city.split()[0]
    if city.find(' ') != -1:
        adm2 = city.split()[1]
        if adm2.find('区') != -1:
            adm2 += '区'  # TODO fix area
    else:
        adm2 = ''

    weather = RealtimeWeather.objects.get(cityName=city_name, adm2=adm2)
    air = RealtimeAirQuality.objects.filter(cityName=city_name, adm2=adm2).first()

    retList = {
        "status": True,
        "message": {
            "time": datetime.now(shanghai_timezone).strftime("%Y-%m-%d %H:%M"),
            "city": city_name + ' ' + adm2,
            "temp": float(weather.temp),
            "text": weather.text,
            "precip": float(weather.precip),
            "wind360": float(weather.wind360),
            "windScale": int(weather.windScale),
            "windSpeed": float(weather.windSpeed),
            "humidity": int(weather.humidity),
            "pressure": int(weather.pressure),
            "aqi": int(air.aqi),
            "category": air.category,
        },
    }
    return JsonResponse(retList, status=200)


@csrf_exempt
@require_http_methods(['GET'])
def get_current_city_info(request: HttpRequest):
    if request.user.is_authenticated:
        user = request.user
        city_name = UserCurrentCity.objects.get(user=user).cityName
        adm2 = UserCurrentCity.objects.get(user=user).adm2
    else:
        city_name = '北京市'
        adm2 = '北京'

    try:
        weather = RealtimeWeather.objects.get(cityName=city_name, adm2=adm2)
    except RealtimeWeather.DoesNotExist:
        weather = RealtimeWeather.objects.first()

    try:
        air = RealtimeAirQuality.objects.filter(cityName=city_name, adm2=adm2).first()
    except RealtimeAirQuality.DoesNotExist:
        air = RealtimeAirQuality.objects.first()

    shanghai_timezone = pytz.timezone('Asia/Shanghai')
    retList = {
        "status": True,
        "message": {
            "time": datetime.now(shanghai_timezone).strftime("%Y-%m-%d %H:%M"),
            "city": city_name + ' ' + adm2,
            "temp": float(weather.temp),
            "text": weather.text,
            "precip": float(weather.precip),
            "wind360": float(weather.wind360),
            "windScale": int(weather.windScale),
            "windSpeed": float(weather.windSpeed),
            "humidity": int(weather.humidity),
            "pressure": int(weather.pressure),
            "aqi": int(air.aqi),
            "category": air.category,
        },
    }
    return JsonResponse(retList, status=200)


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
@login_required
def add_weather_data(request):
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

    response_json = {
        "status": True,
    }
    return JsonResponse(response_json, status=200)


@csrf_exempt
@login_required
def delete_weather_data(request):
    data = json.loads(request.body)
    WeatherInfo.objects.filter(time=data['time'], cityName=str(data['city']).split(' ')[0],adm2=str(data['city']).split(' ')[1]).delete()

    response_json = {
        "status": True,
    }
    return JsonResponse(response_json, status=200)


@csrf_exempt
@login_required
def search_weather_data(request):
    data = json.loads(request.body)
    if data['time']== None:
        data['time']=""
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
        city_filter = Q(cityName__contains=address.split(' ')[0],adm2__contains=address.split(' ')[1]) if address else Q()

        # 执行查询
        weather_data = WeatherInfo.objects.filter(time_filter & city_filter)
        # weather_data = WeatherInfo.objects.filter(
        #     time__range=(from_time, to_time) if from_time and to_time else all,
        #     city__contains=address if address else all
        # )
        weather_data_list = []
        for data in weather_data:
            weather_data_list.append({
                'time': data.time,
                'city': data.cityName+" "+data.adm2,
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


@csrf_exempt
def get_vis_data(request):
    cities = City2CityId.objects.all()

    ret_data = []
    for city in cities:
        # 解析location字段获取经纬度
        lat, lon = map(float, city.location.split(','))

        # print(r"{:.2f},{:.2f}".format(round(lat), round(lon)))

        location_info = LocationToInfo.objects.get(
            location=r"{:.2f},{:.2f}".format(round(lon), round(lat))
        )

        weather_data = {
            "adcode": city.cityId,  # 假设adcode是cityId
            "LON": lon,
            "LAT": lat,
            "temp": float(location_info.temp),
            "precip": float(location_info.precip),
            "aqi": float(location_info.aqi),
            "pressure": float(location_info.pressure),
            "humidity": location_info.humidity,
            "windSpeed": location_info.windSpeed,
            "windScale": location_info.windScale,
            "wind360": location_info.wind360
        }
        ret_data.append(weather_data)

    ## TODO to restore
    return JsonResponse({"data": ret_data}, status=200)


@csrf_exempt
def get_point_data(request):
    lon = request.GET.get("LON")
    lat = request.GET.get("LAT")

    lon = int(float(lon))
    lat = int(float(lat))

    location = str(lon) + ".00," + str(lat) + ".00"
    print(location)

    location_info = LocationToInfo.objects.get(location=location)

    weather_data = {
        "LON": lon,
        "LAT": lat,
        "temp": location_info.temp,
        "precip": location_info.precip,
        "aqi": location_info.aqi,
        "pressure": location_info.pressure,
        "humidity": location_info.humidity,
        "windSpeed": location_info.windSpeed,
        "windScale": location_info.windScale,
        "wind360": location_info.wind360
    }

    return JsonResponse(weather_data, status=200)
