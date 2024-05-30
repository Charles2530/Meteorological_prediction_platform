from django.urls import path
from . import views
from .views import HourlyWeatherView, DailyWeatherView, MonthlyWeatherView

urlpatterns = [
    path('', views.index, name='index'),

    path('manage/data/weather_add/', views.add_weather_data, name='add_weather'),
    path('manage/data/delete/', views.delete_weather_data, name='delete_weather'),
    path('manage/data/search/', views.search_weather_data, name='search_weather'),

    path('weather/overview/', views.overview, name='overview'),
    path('weather/overview_realtime/', views.realtime, name='realtime'),
    path('weather/aqi/', views.aqi_detail, name='aqi_detail'),

    path('weather/rank/', views.rank, name='rank'),
    path('weather/aqi/aqi_change/', views.aqi_current_city_change,
         name='aqi-current-city-change'),

    path('weather/humid/city_change/',
         views.humid_city_change, name='humid-city-change'),
    path('weather/aqi/city_change/', views.aqi_target_city_change,
         name='aqi-target-city-change'),
    path('weather/temp/city_change/',
         views.temp_city_change, name='temp-city-change'),
    path('weather/pressure/city_change/',
         views.pressure_city_change, name='pressure-city-change'),
    path('weather/precip/city_change/',
         views.precip_city_change, name='precip-city-change'),
    path('weather/winSpeed/city_change/',
         views.winspeed_city_change, name='winspeed-city-change'),
    path('weather/temp/city_change/details/',
         views.temp_city_change_detail, name='temp-city-change-detail'),

    path('getProInfo/', views.getProInfo, name='get-pro-info'),  # TODO
    path('operate/current_city/', views.update_current_city, name='update-current-city'),
    path('getHazard/', views.get_hazard, name='get-hazard'),
    path('current/getCityInfo/', views.get_current_city_info),  # TODO
    path('getCityInfo/', views.get_city_info, name='get-city-info'),
    path('getHazardTop/', views.get_top_hazard, name='get-top-hazard'),
    path('vis/getVisData/', views.get_vis_data, name='get-vis-data'),
    path('vis/getPointInfo/', views.get_point_data, name='get-point-info'),
]
