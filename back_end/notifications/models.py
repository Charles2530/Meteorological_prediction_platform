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
    username = models.CharField(max_length=100, verbose_name="用户名")
    city_name = models.CharField(max_length=100, verbose_name="城市名称")
    primary_key = CompositeField([username, city_name], primary_key=True)

    def __str__(self):
        return f"{self.profile.username} - {self.city_name}"

    class Meta:
        models.constraints = [
            models.UniqueConstraint(fields=['username', 'city_name'], name='unique_city_subscription')
        ]
        verbose_name = "城市订阅"
        verbose_name_plural = "城市订阅"


class WeatherForecast(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    img = models.URLField()
    title = models.CharField(max_length=255)
    # date = models.DateTimeField()
    city = models.CharField(max_length=100)
    level = models.IntegerField()
    content = models.TextField()
    instruction = models.TextField()
