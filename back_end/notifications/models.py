from django.contrib.auth.models import User
from django.db import models
from datetime import datetime


class Notification(models.Model):
    pubTime = models.DateTimeField(default=datetime.now)
    place = models.CharField(max_length=100, default="")
    type = models.CharField(max_length=50, default="")
    time = models.DateTimeField()
    level = models.CharField(max_length=10, default="")

    from django.db import models


class CitySubscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="订阅用户")
    city_name = models.CharField(max_length=100, verbose_name="城市名称")
    subscription_time = models.DateTimeField(
        auto_now_add=True, verbose_name="订阅时间")

    def __str__(self):
        return f"{self.user.username} - {self.city_name}"

    class Meta:
        verbose_name = "城市订阅"
        verbose_name_plural = "城市订阅"

class WeatherForecast(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.URLField()
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    city = models.CharField(max_length=100)
    level = models.IntegerField()
    content = models.TextField()
    instruction = models.TextField()

