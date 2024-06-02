# weather/serializers.py

from rest_framework import serializers
from .models import RealtimeAirQuality, HourlyWeather, DailyWeather, MonthlyWeather, WeatherInfo, Pro2City, City2CityId, EarthQuakeInfo, HazardInfo


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


class LocationToInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = City2CityId
        fields = '__all__'


class EarthQuakeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EarthQuakeInfo
        fields = '__all__'


class HazardInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HazardInfo
        fields = '__all__'