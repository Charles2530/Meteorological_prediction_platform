from django.contrib import admin
from .models import HourlyWeather, DailyWeather, MonthlyWeather, Pro2City, City2CityId, ProGeography, WeatherInfo

# Register your models here.
admin.site.register(HourlyWeather)
admin.site.register(DailyWeather)
admin.site.register(MonthlyWeather)
admin.site.register(Pro2City)
admin.site.register(City2CityId)
admin.site.register(ProGeography)
admin.site.register(WeatherInfo)
