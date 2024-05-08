from django.db import models
from datetime import datetime

# Create your models here.
class HourlyWeather(models.Model):
    fxTime = models.DateTimeField(default=datetime.now)
    temp = models.FloatField(default=0.0)
    icon = models.CharField(max_length=10, default="")
    text = models.CharField(max_length=200, default="")
    wind360 = models.FloatField(default=0.0)
    windDir = models.CharField(max_length=20, default="")
    windScale = models.CharField(max_length=10, default="")
    windSpeed = models.FloatField(default=0.0)
    humidity = models.FloatField(default=0.0)
    pop = models.FloatField(default=0.0)  # Probability of precipitation
    precip = models.FloatField(default=0.0)
    pressure = models.FloatField(default=0.0)
    cloud = models.FloatField(default=0.0)
    dew = models.FloatField(default=0.0)

    def __str__(self):
        return "hourly weather for " + self.fxTime.strftime('%Y-%m-%d %H:%M:%S')


class DailyWeather(models.Model):
    fxDate = models.DateField(default=datetime.now)
    sunrise = models.DateTimeField(default=datetime.now)
    sunset = models.DateTimeField(default=datetime.now)
    moonrise = models.DateTimeField(default=datetime.now)
    moonset = models.DateTimeField(default=datetime.now)
    moonPhase = models.CharField(max_length=10, default="")
    moonPhaseIcon = models.CharField(max_length=10, default="")
    tempMax = models.FloatField(default=0.0)
    tempMin = models.FloatField(default=0.0)
    iconDay = models.CharField(max_length=10, default="")
    textDay = models.CharField(max_length=50, default="")
    iconNight = models.CharField(max_length=10, default="")
    textNight = models.CharField(max_length=50, default="")
    wind360Day = models.FloatField(default=0.0)
    windDirDay = models.CharField(max_length=20, default="")
    windScaleDay = models.CharField(max_length=10, default="")
    windSpeedDay = models.FloatField(default=0.0)
    wind360Night = models.FloatField(default=0.0)
    windDirNight = models.CharField(max_length=20, default="")
    windScaleNight = models.CharField(max_length=10, default="")
    windSpeedNight = models.FloatField(default=0.0)
    humidity = models.FloatField(default=0.0)
    precip = models.FloatField(default=0.0)
    pressure = models.FloatField(default=0.0)
    vis = models.FloatField(default=0.0)
    cloud = models.IntegerField(default=0)
    uvIndex = models.IntegerField(default=0)

    def __str__(self):
        return "daily weather for " + str(self.fxDate) + " at location"


class MonthlyWeather(models.Model):
    month_time = models.DateTimeField(default=datetime.now)
    location = models.CharField(max_length=200, default="")
    average_temperature = models.FloatField(default=0.0)
    average_humidity = models.FloatField(default=0.0)
    average_pressure = models.FloatField(default=0.0)
    average_wind_speed = models.FloatField(default=0.0)
    average_wind_direction = models.FloatField(default=0.0)
    average_cloud_cover = models.FloatField(default=0.0)
    average_precipitation = models.FloatField(default=0.0)
    text = models.CharField(max_length=200, default="")

    def __str__(self):
        return "monthly weather for " + self.month_time.strftime('%Y-%m-%d %H:%M:%S') + " " + self.location
        return "monthly weather for " + self.month_time.strftime('%Y-%m-%d %H:%M:%S') + " " + self.location

### TODO pro2city data
class Pro2City(models.Model):
    proName = models.CharField(max_length=200, default="")
    cityId = models.CharField(default=0)

### TODO pro2city data
class City2CityId(models.Model):
    cityName = models.CharField(max_length=200, default="")
    cityId = models.CharField(default=0)


### TODO pro_geography data
class ProGeography(models.Model):
    proName = models.CharField(max_length=200, default="")
    geographyInfo = models.CharField(max_length=2000)
