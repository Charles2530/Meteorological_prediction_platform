from django.db import models
from datetime import datetime

from django.contrib.auth.models import User


class Notification(models.Model):
    pubTime = models.DateTimeField(default=datetime.now)
    place = models.CharField(max_length=100, default="")
    type = models.CharField(max_length=50, default="")
    time = models.DateTimeField()
    level = models.CharField(max_length=10, default="")

    class Meta:
        verbose_name = "灾害订阅"
        verbose_name_plural = "灾害订阅"


class CitySubscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="订阅用户", default=None)
    cityName = models.CharField(max_length=40, verbose_name="城市名称")
    adm2 = models.CharField(max_length=40, verbose_name="二级行政区域名称", default="")

    def __str__(self):
        return f"{self.user.username} - {self.cityName} - {self.adm2}"

    class Meta:
        verbose_name = "用户订阅城市表"
        verbose_name_plural = "用户订阅城市表"


class WeatherForecast(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    img = models.URLField()
    title = models.CharField(max_length=255)
    # date = models.DateTimeField()
    city = models.CharField(max_length=40)
    adm2 = models.CharField(max_length=40, default='')
    level = models.IntegerField(default=0)
    content = models.TextField()
    instruction = models.TextField()

    def __str__(self):
        return f"{self.city} - {self.adm2}"

    class Meta:
        verbose_name = "天气预报"
        verbose_name_plural = "天气预报"
