# weather/serializers.py

from rest_framework import serializers
from .models import HourlyWeather, DailyWeather, MonthlyWeather, WeatherInfo, Pro2City, City2CityId


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


# class WeatherInfo(models.Model):
class WeatherInfoSerializer(serializers.Serializer):
    class Meta:
        model = WeatherInfo
        fields = '__all__'


class Pro2CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pro2City
        fields = '__all__'


class City2CityIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = City2CityId
        fields = '__all__'