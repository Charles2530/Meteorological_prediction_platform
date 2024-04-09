from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import HourlyWeather, DailyWeather, MonthlyWeather
from .serializers import HourlyWeatherSerializer, DailyWeatherSerializer, MonthlyWeatherSerializer


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

'''
The following views are my exercises for the weather app.
'''

def index(request):
    return HttpResponse("Welcome to the weather app!")

# def home(request):
#     path = request.path
#     response = HttpResponse("Welcome to the home page!")
#     return HttpResponse(path, content_type='text/html', charset='utf-8')
