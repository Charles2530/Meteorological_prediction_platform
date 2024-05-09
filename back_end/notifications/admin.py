from django.contrib import admin
from .models import Notification, CitySubscription, WeatherForecast

# Register your models here.
admin.site.register(Notification)
admin.site.register(CitySubscription)
admin.site.register(WeatherForecast)
