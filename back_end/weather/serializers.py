# weather/serializers.py

from rest_framework import serializers
from .models import RealtimeWeather, RealtimeAirQuality
from .models import HourlyWeather, DailyWeather, MonthlyWeather, WeatherInfo
from .models import Pro2City, City2CityId, ProGeography, LocationToInfo
from .models import EarthQuakeInfo, HazardInfo


class RealtimeWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealtimeAirQuality
        fields = '__all__'


class RealtimeAirQualitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RealtimeAirQuality
        fields = '__all__'


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


class ProGeographySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProGeography
        fields = '__all__'


class LocationToInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationToInfo
        fields = '__all__'


class EarthQuakeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EarthQuakeInfo
        fields = '__all__'


class HazardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HazardInfo
        fields = '__all__'