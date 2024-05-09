from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
import json
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Notification, WeatherForecast, CitySubscription
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NotificationSerializer, CitySubscriptionSerializer, WeatherForecastSerializer
from .task import fetch_catastrophic_forecast_cities_list, fetch_weather_catastrophic_forecast
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.



class NotificationView(APIView):
    def get(self, request, format=None):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class CitySubscriptionView(APIView):
    def get(self, request, format=None):
        city_subscriptions = CitySubscription.objects.all()
        serializer = CitySubscriptionSerializer(city_subscriptions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CitySubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class WeatherForecastView(APIView):
    def get(self, request, format=None):
        weather_forecast = WeatherForecast.objects.all()
        serializer = WeatherForecastSerializer(weather_forecast, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = WeatherForecastSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


def get_alarm_notice(request):
    locations = WeatherForecast.objects.all()
    response_json = {
        "success": True,
        "notifications": []
    }
    
    # user = User.objects.filter(username=settings.CURRENT_UNAME).first()
    user = request.user
    cities = CitySubscription.objects.filter(user=user)
    for forecast in locations:
        for city in cities:
            if city.city_name in forecast.city:
                forecast_json = {
                    "id": forecast.id,
                    # TODO:change pic
                    # "img": "https://ts1.cn.mm.bing.net/th/id/R-C.5b318dcf92724f1b99c194f891602f06?rik=eg7%2f2A2FtTorZA&riu=http%3a%2f%2fappdata.langya.cn%2fuploadfile%2f2020%2f0722%2f20200722090230374.jpg&ehk=DTXD%2bpXZoXFP8PBVpZeox9lN%2f5eoUhdebZg6f1gIPs0%3d&risl=&pid=ImgRaw&r=0",
                    "img": forecast.img,
                    "title": forecast.title,
                    "date": "2024-10-24",
                    "city": city,
                    "level": forecast.level,
                    "content": forecast.content,
                    "instruction": forecast.instruction,
                }
                response_json['notifications'].append(forecast_json)
                break
    return JsonResponse(response_json, status=200)

@csrf_exempt
# @require_http_methods(['POST'])
def subscribe(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cities = data.get('cities')
            # user = User.objects.filter(username=settings.CURRENT_UNAME).first()
            user = request.user
            # return JsonResponse({'status': settings.CURRENT_UNAME, 'message': user}, status=400)
            if not cities:
                return JsonResponse({'status': False, 'message': 'No cities provided.'}, status=400)

            city_obj, created = CitySubscription.objects.update_or_create(
                user=user,
                city_name=cities,
            )
            city_obj.save()

            return JsonResponse({'status': True})
        except json.JSONDecodeError:
            return JsonResponse({'status': False, 'message': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': False, 'message': str(e)}, status=500)
    else:
        response_json = {
            "success": True,
            "tableData": []
        }
        # user = User.objects.filter(username=settings.CURRENT_UNAME).first()
        user = request.user
        cities = CitySubscription.objects.filter(user=user)
        for city in cities:
            city_json = {
                "city": city.city_name,
                "status": "已订阅",
            }
            response_json['tableData'].append(city_json)
        return JsonResponse(response_json, status=200)

def get_brief(request):
    locations = WeatherForecast.objects.all()
    response_json = {
        "success": True,
        "notifications": []
    }
    # user = User.objects.filter(username=settings.CURRENT_UNAME).first()
    user = request.user
    cities = CitySubscription.objects.filter(user=user)
    for forecast in locations:
        # forecast = fetch_weather_catastrophic_forecast(location=locationId)
        for city in cities:
            if city.city_name in forecast.city:
                forecast_json = {
                    "id": forecast.id,
                    # TODO:change pic
                    "img": forecast.img,
                    "date": forecast.title,
                    "date": "2024-05-10",
                    "city": city,
                }
                response_json['notifications'].append(forecast_json)
                break
    return JsonResponse(response_json, status=200)

def get_alarm_level(request):
    locations = WeatherForecast.objects.all()
    response_json = {
        "success": True,
        "cnt": []
    }
    count = {}
    for idx in range(1, 6):
        count[idx] = 0
    for forecast in locations:
        # forecast = fetch_weather_catastrophic_forecast(location=locationId)
        count[forecast.level] += 1
    for idx in range(1, 6):
        response_json['cnt'].append(count[idx])
    return JsonResponse(response_json, status=200)

def get_recent(request):
    locations = WeatherForecast.objects.all()
    response_json = {
        "success": True,
        "notifications": []
    }
    for (idx,forecast) in enumerate(locations):
        # forecast = fetch_weather_catastrophic_forecast(location=locationId)
        # forecast = forecast["warning"]
        # return JsonResponse(forecast, status=400)
        forecast_json = {
            "id": forecast.id,
            # TODO:change pic
            "img": forecast.img,
            "title": forecast.title,
            # "date": forecast.date,
            "date": "2024-05-10",
            "city": forecast.city,
            "level": forecast.level,
            "content": forecast.content,
            "instruction": forecast.instruction,
        }
        response_json['notifications'].append(forecast_json)
        if idx == 3:
            break
    return JsonResponse(response_json, status=200)

def get_notification_data():
    notifications = []
    for notification_data in notifications:
        city_name = notification_data['city']
        city_subscription = CitySubscription.objects.filter(
            city_name=city_name).first()
        if city_subscription:
            notification_data['city'] = city_subscription
            Notification.objects.create(**notification_data)