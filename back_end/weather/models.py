from django.db import models
from datetime import datetime


# Create your models here.
class RealtimeWeather(models.Model):
    cityName = models.CharField(max_length=40, default='北京市')
    adm2 = models.CharField(max_length=40, default='北京')
    temp = models.IntegerField()
    feelsLike = models.IntegerField()
    icon = models.CharField(max_length=20)
    text = models.CharField(max_length=20)
    wind360 = models.IntegerField()
    windDir = models.CharField(max_length=20)
    windScale = models.CharField(max_length=20)
    windSpeed = models.IntegerField()
    humidity = models.IntegerField()
    precip = models.FloatField()
    pressure = models.IntegerField()

    def __str__(self):
        return f"{self.cityName} - {self.adm2}"

    class Meta:
        # unique_together = ('cityName', 'adm2')
        # constraints = [
        #     models.UniqueConstraint(fields=['cityName', 'adm2'], name='unique_city_adm2_in_RealtimeWeather')
        # ]

        verbose_name = "实时天气"
        verbose_name_plural = "实时天气"


class RealtimeAirQuality(models.Model):
    cityName = models.CharField(max_length=40, default='北京市')
    adm2 = models.CharField(max_length=40, default='北京')
    aqi = models.IntegerField()
    level = models.IntegerField()
    category = models.CharField(max_length=10)
    pm10 = models.CharField(max_length=10)
    pm2p5 = models.CharField(max_length=10)
    no2 = models.CharField(max_length=10)
    so2 = models.CharField(max_length=10)
    co = models.CharField(max_length=10)
    o3 = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.cityName} - {self.adm2}"

    class Meta:
        # unique_together = ('cityName', 'adm2')
        # constraints = [
        #     models.UniqueConstraint(fields=['cityName', 'adm2'], name='unique_city_adm2_in_RealtimeAirQuality')
        # ]

        verbose_name = "实时空气质量"
        verbose_name_plural = "实时空气质量"


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

    class Meta:
        verbose_name = "每小时天气（废弃）"
        verbose_name_plural = "每小时天气（废弃）"


class DailyWeather(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=40, default="北京市")
    adm2 = models.CharField(max_length=40, default='北京')
    fxDate = models.DateField(default=datetime.now)
    sunrise = models.CharField(max_length=40, default='')
    sunset = models.CharField(max_length=40, default='')
    # moonrise = models.DateTimeField(default=datetime.now)
    # moonset = models.DateTimeField(default=datetime.now)
    # moonPhase = models.CharField(max_length=10, default="")
    # moonPhaseIcon = models.CharField(max_length=10, default="")
    tempMax = models.IntegerField(default=0)
    tempMin = models.IntegerField(default=0)
    # iconDay = models.CharField(max_length=10, default="")
    # textDay = models.CharField(max_length=50, default="")
    # iconNight = models.CharField(max_length=10, default="")
    # textNight = models.CharField(max_length=50, default="")
    # wind360Day = models.FloatField(default=0.0)
    # windDirDay = models.CharField(max_length=20, default="")
    # windScaleDay = models.CharField(max_length=10, default="")
    windSpeedDay = models.CharField(max_length=10, default="")
    # wind360Night = models.FloatField(default=0.0)
    # windDirNight = models.CharField(max_length=20, default="")
    # windScaleNight = models.CharField(max_length=10, default="")
    # windSpeedNight = models.FloatField(default=0.0)
    humidity = models.FloatField(default=0.0)
    precip = models.FloatField(default=0.0)
    pressure = models.FloatField(default=0.0)
    vis = models.FloatField(default=0.0)
    cloud = models.IntegerField(default=0)
    uvIndex = models.IntegerField(default=0)
    aqi = models.IntegerField(default=0)

    def __str__(self):
        return "daily weather for " + str(self.fxDate) + " at location"

    class Meta:
        verbose_name = "每日天气"
        verbose_name_plural = "每日天气"


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

    class Meta:
        verbose_name = "每月天气"
        verbose_name_plural = "每月天气"


# TODO pro2city data


class Pro2City(models.Model):
    proName = models.CharField(max_length=20, primary_key=True)
    cityId = models.CharField(max_length=20)

    class Meta:
        verbose_name = "省份省会"
        verbose_name_plural = "省份省会"


# TODO pro2city data


class City2CityId(models.Model):
    cityId = models.CharField(max_length=20, primary_key=True)
    cityName = models.CharField(max_length=40)
    areaName = models.CharField(max_length=40, default="")
    location = models.CharField(max_length=40, default="non_location_info")

    def __str__(self):
        return f"{self.cityName} - {self.areaName} - {self.cityId} - {self.location}"

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = "城市"


# TODO pro_geography data
class ProGeography(models.Model):
    proName = models.CharField(primary_key=True, max_length=20)
    geographyInfo = models.TextField(max_length=2000)

    def __str__(self):
        return self.proName

    class Meta:
        verbose_name = "城市地理信息"
        verbose_name_plural = "城市地理信息"


# {
#     "time": "2020-07-25 00:00",
#     "city": "北京",
#     "temp": "28",
#     "text": "晴",
#     "precip": "0.0",
#     "wind360": "246",
#     "windScale": "2",
#     "windSpeed": "8",
#     "humidity": "49",
#     "pressure": "1001",
#     "aqi": "52",
#     "category": "良",
# },

class WeatherInfo(models.Model):
    # hourly
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(default=datetime.now)
    cityName = models.CharField(max_length=40, default="北京市")
    adm2 = models.CharField(max_length=40, default='北京')
    temp = models.IntegerField(default=0)
    text = models.CharField(max_length=10, default="")
    precip = models.FloatField(default=0.0)
    wind360 = models.IntegerField(default=0)
    windScale = models.CharField(max_length=5, default="0")
    windSpeed = models.IntegerField(default=0)
    humidity = models.IntegerField(default=0)
    pressure = models.IntegerField(default=0)
    aqi = models.IntegerField(default=0)
    category = models.CharField(max_length=5, default="")

    def __str__(self):
        return "weather info for " + self.cityName + " " + self.time.strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        # unique_together = ('time', 'cityName', 'adm2')
        # constraints = [
        #     models.UniqueConstraint(fields=['time', 'cityName', 'adm2'], name='unique_time_city_adm2')
        # ]

        verbose_name = "每小时天气"
        verbose_name_plural = "每小时天气"


class LocationToInfo(models.Model):
    lon = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)
    location = models.CharField(max_length=40, default="", primary_key=True)
    obsTime = models.CharField(max_length=40, default="2021-12-16T10:00+00:00")
    aqi = models.IntegerField(default=0)
    temp = models.CharField(max_length=40, default="21")
    text = models.CharField(max_length=40, default=0)
    wind360 = models.CharField(max_length=40, default="287")
    windDir = models.CharField(max_length=40, default="西北风")
    windScale = models.CharField(max_length=40, default="2")
    windSpeed = models.CharField(max_length=40, default="10")
    humidity = models.CharField(max_length=40, default="27")
    precip = models.CharField(max_length=40, default="0.0")
    pressure = models.CharField(max_length=40, default="1021")

    class Meta:
        verbose_name = "格点天气"
        verbose_name_plural = "格点天气"


class EarthQuakeInfo(models.Model):
    level = models.CharField(max_length=40, default="")
    time = models.CharField(max_length=40, default="")
    lat = models.CharField(max_length=40, default="")
    lon = models.CharField(max_length=40, default="")
    depth = models.CharField(max_length=40, default="")
    key = models.CharField(max_length=80, default="", primary_key=True)
    location = models.CharField(max_length=40, default="")

    class Meta:
        verbose_name = "地震信息"
        verbose_name_plural = "地震信息"


class HazardInfo(models.Model):
    location = models.CharField(max_length=40, default='', primary_key=True)
    cityName = models.CharField(max_length=40, default='')
    adm2 = models.CharField(max_length=40, default='')
    typeName = models.CharField(max_length=15)
    time = models.DateTimeField()  # update by pubTime
    severity = models.CharField(max_length=15)
    severityColor = models.CharField(max_length=15)

    class Meta:
        verbose_name = "灾害信息"
        verbose_name_plural = "灾害信息"
