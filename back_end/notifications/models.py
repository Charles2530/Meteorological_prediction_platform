# from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

from users.models import Profile


class Notification(models.Model):
    pubTime = models.DateTimeField(default=datetime.now)
    place = models.CharField(max_length=100, default="")
    type = models.CharField(max_length=50, default="")
    time = models.DateTimeField()
    level = models.CharField(max_length=10, default="")


class CitySubscription(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name="订阅用户", default=None)
    cityName = models.CharField(max_length=40, verbose_name="城市名称")

    def __str__(self):
        return f"{self.profile.username} - {self.cityName}"

    class Meta:
        verbose_name = "城市订阅"
        verbose_name_plural = "城市订阅"


class WeatherForecast(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    img = models.URLField()
    title = models.CharField(max_length=255)
    # date = models.DateTimeField()
    city = models.CharField(max_length=100)
    level = models.IntegerField()
    content = models.TextField()
    instruction = models.TextField()
