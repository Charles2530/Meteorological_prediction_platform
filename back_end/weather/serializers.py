# myapp/serializers.py

from rest_framework import serializers
from .models import HourlyWeather, DailyWeather, MonthlyWeather


class HourlyWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourlyWeather
        fields = '__all__'


class DailyWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyWeather
        fields = '__all__'


class MonthlyWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyWeather
        fields = '__all__'