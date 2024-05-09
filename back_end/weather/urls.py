from django.urls import path
from . import views
from .views import HourlyWeatherView, DailyWeatherView, MonthlyWeatherView


urlpatterns = [
    path('', views.index, name='index'),

    path('manage/data/weather_add/', views.add_weather_data, name='add_weather'),
    path('manage/data/delete/', views.delete_weather_data, name='delete_weather'),
    path('manage/data/search/', views.search_weather_data, name='search_weather'),


    path('weather/overview/', views.overview, name='overview'),
    path('weather/30days/', views.thirty_days_forecast, name='30days-forecast'),
    path('weather/overview_realtime/', views.realtime, name='realtime'),

    path('weather/aqi/rank_best/', views.aqi_best, name='aqi-best'),
    path('weather/aqi/rank_worst/', views.aqi_worst, name='aqi-worst'),
    path('weather/aqi/aqi_change/', views.aqi_current_city_change,
         name='aqi-current-city-change'),

    path('weather/humid/city_change/',
         views.humid_city_change, name='humid-city-change'),
    path('weather/aqi/city_change/', views.aqi_target_city_change,
         name='aqi-target-city-change'),
    path('temp/aqi/city_change/', views.temp_city_change, name='temp-city-change'),
    path('temp/pressure/city_change/',
         views.pressure_city_change, name='pressure-city-change'),

    # path('getProInfo/', views.getProInfo, name='get-pro-info'), # TODO
    # path('getHazard/', views.getHazard), #TODO
    # path('getCityInfo', views.getCityInfo), #TODO
]
