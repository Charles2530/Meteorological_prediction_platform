from rest_framework import serializers
from .models import Notification, WeatherForecast, CitySubscription


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class WeatherForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = '__all__'

class CitySubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitySubscription
        fields = '__all__'