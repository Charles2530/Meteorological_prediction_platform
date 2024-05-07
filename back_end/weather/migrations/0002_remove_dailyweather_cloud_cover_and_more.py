# Generated by Django 5.0.4 on 2024-05-06 12:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("weather", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dailyweather",
            name="cloud_cover",
        ),
        migrations.RemoveField(
            model_name="dailyweather",
            name="date_time",
        ),
        migrations.RemoveField(
            model_name="dailyweather",
            name="location",
        ),
        migrations.RemoveField(
            model_name="dailyweather",
            name="precipitation",
        ),
        migrations.RemoveField(
            model_name="dailyweather",
            name="temperature",
        ),
        migrations.RemoveField(
            model_name="dailyweather",
            name="weather_description",
        ),
        migrations.RemoveField(
            model_name="dailyweather",
            name="wind_direction",
        ),
        migrations.RemoveField(
            model_name="dailyweather",
            name="wind_speed",
        ),
        migrations.RemoveField(
            model_name="hourlyweather",
            name="cloud_cover",
        ),
        migrations.RemoveField(
            model_name="hourlyweather",
            name="hour_time",
        ),
        migrations.RemoveField(
            model_name="hourlyweather",
            name="location",
        ),
        migrations.RemoveField(
            model_name="hourlyweather",
            name="precipitation",
        ),
        migrations.RemoveField(
            model_name="hourlyweather",
            name="temperature",
        ),
        migrations.RemoveField(
            model_name="hourlyweather",
            name="weather_description",
        ),
        migrations.RemoveField(
            model_name="hourlyweather",
            name="wind_direction",
        ),
        migrations.RemoveField(
            model_name="hourlyweather",
            name="wind_speed",
        ),
        migrations.RemoveField(
            model_name="monthlyweather",
            name="weather_description",
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="cloud",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="fxDate",
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="iconDay",
            field=models.CharField(default="", max_length=10),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="iconNight",
            field=models.CharField(default="", max_length=10),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="moonPhase",
            field=models.CharField(default="", max_length=10),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="moonPhaseIcon",
            field=models.CharField(default="", max_length=10),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="moonrise",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="moonset",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="precip",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="sunrise",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="sunset",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="tempMax",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="tempMin",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="textDay",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="textNight",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="uvIndex",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="vis",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="wind360Day",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="wind360Night",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="windDirDay",
            field=models.CharField(default="", max_length=20),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="windDirNight",
            field=models.CharField(default="", max_length=20),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="windScaleDay",
            field=models.CharField(default="", max_length=10),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="windScaleNight",
            field=models.CharField(default="", max_length=10),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="windSpeedDay",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="dailyweather",
            name="windSpeedNight",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="hourlyweather",
            name="cloud",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="hourlyweather",
            name="dew",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="hourlyweather",
            name="fxTime",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name="hourlyweather",
            name="icon",
            field=models.CharField(default="", max_length=10),
        ),
        migrations.AddField(
            model_name="hourlyweather",
            name="pop",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="hourlyweather",
            name="precip",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="hourlyweather",
            name="temp",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="hourlyweather",
            name="text",
            field=models.CharField(default="", max_length=200),
        ),
        migrations.AddField(
            model_name="hourlyweather",
            name="wind360",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="hourlyweather",
            name="windDir",
            field=models.CharField(default="", max_length=20),
        ),
        migrations.AddField(
            model_name="hourlyweather",
            name="windScale",
            field=models.CharField(default="", max_length=10),
        ),
        migrations.AddField(
            model_name="hourlyweather",
            name="windSpeed",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="monthlyweather",
            name="text",
            field=models.CharField(default="", max_length=200),
        ),
        migrations.AlterField(
            model_name="dailyweather",
            name="humidity",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="dailyweather",
            name="pressure",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="hourlyweather",
            name="humidity",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="hourlyweather",
            name="pressure",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="monthlyweather",
            name="average_cloud_cover",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="monthlyweather",
            name="average_humidity",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="monthlyweather",
            name="average_precipitation",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="monthlyweather",
            name="average_pressure",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="monthlyweather",
            name="average_temperature",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="monthlyweather",
            name="average_wind_direction",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="monthlyweather",
            name="average_wind_speed",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="monthlyweather",
            name="location",
            field=models.CharField(default="", max_length=200),
        ),
        migrations.AlterField(
            model_name="monthlyweather",
            name="month_time",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
