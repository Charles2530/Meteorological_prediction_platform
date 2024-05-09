from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
import json
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Notification,WeatherForecast,CitySubscription
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NotificationSerializer
from .task import fetch_catastrophic_forecast_cities_list, fetch_weather_catastrophic_forecast
from django.http import HttpResponse, JsonResponse
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


def get_alarm_notice(request):
    cities = fetch_catastrophic_forecast_cities_list()
    locations = cities['warningLocList']
    response_json = {
        "success": True,
        "notifications": []
    }
    user = User.objects.filter(username=settings.CURRENT_UNAME).first()
    cities = CitySubscription.objects.filter(user=user)
    for locationId in locations:
        forecast = fetch_weather_catastrophic_forecast(location=locationId)
        for city in cities:
            if forecast['sender'].contain(city.city_name):
                forecast_json = {
                    "id": forecast['id'],
                    # TODO:change pic
                    "img": "https://ts1.cn.mm.bing.net/th/id/R-C.5b318dcf92724f1b99c194f891602f06?rik=eg7%2f2A2FtTorZA&riu=http%3a%2f%2fappdata.langya.cn%2fuploadfile%2f2020%2f0722%2f20200722090230374.jpg&ehk=DTXD%2bpXZoXFP8PBVpZeox9lN%2f5eoUhdebZg6f1gIPs0%3d&risl=&pid=ImgRaw&r=0",
                    "title": forecast['title'],
                    "date": forecast['startTime'],
                    "city": city,
                    "level": getLevel(forecast['severity']),
                    "content": forecast['text'],
                    "instruction": "请有关单位和人员做好防范准备。"
                }
                response_json['notifications'].append(forecast_json)
                break
    return JsonResponse(response_json, status=200)


@require_http_methods(['POST'])
def subscribe(request):
    try:
        data = json.loads(request.body)
        cities = data.get('cities')
        user = User.objects.filter(username=settings.CURRENT_UNAME).first()

        if not cities:
            return JsonResponse({'status': False, 'message': 'No cities provided.'}, status=400)

        for city in cities:
            city_obj, created = CitySubscription.objects.update_or_create(
                user=user,
                city_name=city,
                defaults={'subscription_date': timezone.now()}
            )

            if not created:
                city_obj.delete()

        return JsonResponse({'status': True})
    except json.JSONDecodeError:
        return JsonResponse({'status': False, 'message': 'Invalid JSON data.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=500)


@require_http_methods(['GET'])
def subscribe(request):
    response_json = {
        "success": True,
        "tableData": []
    }
    user = User.objects.filter(username=settings.CURRENT_UNAME).first()
    cities = CitySubscription.objects.filter(user=user)
    for city in cities:
        city_json = {
            "city": city.city_name,
            "status": "已订阅",
        }
        response_json['tableData'].append(city_json)
    return JsonResponse(response_json, status=200)


def get_brief(request):
    cities = fetch_catastrophic_forecast_cities_list()
    locations = cities['warningLocList']
    response_json = {
        "success": True,
        "notifications": []
    }
    user = User.objects.filter(username=settings.CURRENT_UNAME).first()
    cities = CitySubscription.objects.filter(user=user)
    for locationId in locations:
        forecast = fetch_weather_catastrophic_forecast(location=locationId)
        for city in cities:
            if forecast['sender'].contain(city.city_name):
                forecast_json = {
                    "id": forecast['id'],
                    # TODO:change pic
                    "img": "https://ts1.cn.mm.bing.net/th/id/R-C.5b318dcf92724f1b99c194f891602f06?rik=eg7%2f2A2FtTorZA&riu=http%3a%2f%2fappdata.langya.cn%2fuploadfile%2f2020%2f0722%2f20200722090230374.jpg&ehk=DTXD%2bpXZoXFP8PBVpZeox9lN%2f5eoUhdebZg6f1gIPs0%3d&risl=&pid=ImgRaw&r=0",
                    "title": forecast['title'],
                    "date": forecast['startTime'],
                    "city": forecast['sender'],
                }
                response_json['notifications'].append(forecast_json)
    return JsonResponse(response_json, status=200)


def get_alarm_level(request):
    cities = fetch_catastrophic_forecast_cities_list()
    locations = cities['warningLocList']
    response_json = {
        "success": True,
        "cnt": []
    }
    count = {}
    for idx in range(1, 6):
        count[idx] = 0
    for locationId in locations:
        forecast = fetch_weather_catastrophic_forecast(location=locationId)
        count[getLevel(forecast['severity'])] += 1
    for idx in range(1, 6):
        response_json['cnt'].append(count[idx])
    return JsonResponse(response_json, status=200)


def get_recent(request):
    cities = fetch_catastrophic_forecast_cities_list()
    locations = cities['warningLocList']
    response_json = {
        "success": True,
        "notifications": []
    }
    for (locationId, idx) in enumerate(locations):
        forecast = fetch_weather_catastrophic_forecast(location=locationId)
        forecast = forecast["warning"]
        forecast_json = {
            "id": forecast["id"],
            # TODO:change pic
            "img": "https://ts1.cn.mm.bing.net/th/id/R-C.5b318dcf92724f1b99c194f891602f06?rik=eg7%2f2A2FtTorZA&riu=http%3a%2f%2fappdata.langya.cn%2fuploadfile%2f2020%2f0722%2f20200722090230374.jpg&ehk=DTXD%2bpXZoXFP8PBVpZeox9lN%2f5eoUhdebZg6f1gIPs0%3d&risl=&pid=ImgRaw&r=0",
            "title": forecast['title'],
            "date": forecast['startTime'],
            "city": forecast['sender'],
            "level": getLevel(forecast['severity']),
            "content": forecast['text'],
            "instruction": "请有关单位和人员做好防范准备。"
        }
        response_json['notifications'].append(forecast_json)
        if idx == 3:
            break
    return JsonResponse(response_json, status=200)

def get_notification_data():
    notifications = []  

    for notification_data in notifications:
        city_name = notification_data['city']
        city_subscription = CitySubscription.objects.filter(city_name=city_name).first()
        if city_subscription:
            notification_data['city'] = city_subscription
            Notification.objects.create(**notification_data)

def get_weather_forecast_data():
    forecasts = []  

    for forecast_data in forecasts:
        WeatherForecast.objects.create(**forecast_data)

def notification_view(request):
    get_notification_data()

    notifications = Notification.objects.all()
    serializer = NotificationSerializer(notifications, many=True)
    return JsonResponse(serializer.data, safe=False)

def weather_forecast_view(request):
    get_weather_forecast_data()

    forecasts = WeatherForecast.objects.all()
    serialized_data = []

    return JsonResponse(serialized_data, safe=False)