from django.db import models


# Create your models here.
class HourlyWeather(models.Model):
    hour_time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200)
    temperature = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField()
    wind_speed = models.FloatField()
    wind_direction = models.FloatField()
    cloud_cover = models.FloatField()
    precipitation = models.FloatField()
    weather_description = models.CharField(max_length=200)

    def __str__(self):
        return "hourly weather for " + self.hour_time.strftime('%Y-%m-%d %H:%M:%S') + " " + self.location


class DailyWeather(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200)
    temperature = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField()
    wind_speed = models.FloatField()
    wind_direction = models.FloatField()
    cloud_cover = models.FloatField()
    precipitation = models.FloatField()
    weather_description = models.CharField(max_length=200)

    def __str__(self):
        return "daliy weather for " + self.date_time.strftime('%Y-%m-%d %H:%M:%S') + " " + self.location


class MonthlyWeather(models.Model):
    month_time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200)
    average_temperature = models.FloatField()
    average_humidity = models.FloatField()
    average_pressure = models.FloatField()
    average_wind_speed = models.FloatField()
    average_wind_direction = models.FloatField()
    average_cloud_cover = models.FloatField()
    average_precipitation = models.FloatField()
    weather_description = models.CharField(max_length=200)

    def __str__(self):
        return "monthly weather for " + self.month_time.strftime('%Y-%m-%d %H:%M:%S') + " " + self.location