from django.contrib import admin
from .models import RealtimeWeather, RealtimeAirQuality
from .models import HourlyWeather, DailyWeather, MonthlyWeather, WeatherInfo
from .models import Pro2City, City2CityId, ProGeography, LocationToInfo
from .models import EarthQuakeInfo, HazardInfo


# Register your models here.
admin.site.register(RealtimeWeather)
admin.site.register(RealtimeAirQuality)
admin.site.register(HourlyWeather)
admin.site.register(DailyWeather)
admin.site.register(MonthlyWeather)
admin.site.register(WeatherInfo)
admin.site.register(Pro2City)
admin.site.register(City2CityId)
admin.site.register(ProGeography)
admin.site.register(LocationToInfo)
admin.site.register(EarthQuakeInfo)
admin.site.register(HazardInfo)
