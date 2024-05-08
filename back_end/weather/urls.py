from django.urls import path
from . import views
from .views import HourlyWeatherView, DailyWeatherView, MonthlyWeatherView



urlpatterns = [
    path('', views.index, name='index'),
    # path('data/weather_add', views.add_weather, name='add_weather'),
    path('hourly/', DailyWeatherView.as_view(), name='hourly-weather'),
    path('daily/', HourlyWeatherView.as_view(), name='daily-weather'),
    path('monthly/', MonthlyWeatherView.as_view(), name='monthly-weather'),
    path('getProInfo/', views.getProInfo, name='get-pro-info'),
]