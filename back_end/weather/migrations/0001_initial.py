# Generated by Django 5.0.3 on 2024-04-05 13:18

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DailyWeather",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_time", models.DateTimeField(auto_now_add=True)),
                ("location", models.CharField(max_length=200)),
                ("temperature", models.FloatField()),
                ("humidity", models.FloatField()),
                ("pressure", models.FloatField()),
                ("wind_speed", models.FloatField()),
                ("wind_direction", models.FloatField()),
                ("cloud_cover", models.FloatField()),
                ("precipitation", models.FloatField()),
                ("weather_description", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="HourlyWeather",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hour_time", models.DateTimeField(auto_now_add=True)),
                ("location", models.CharField(max_length=200)),
                ("temperature", models.FloatField()),
                ("humidity", models.FloatField()),
                ("pressure", models.FloatField()),
                ("wind_speed", models.FloatField()),
                ("wind_direction", models.FloatField()),
                ("cloud_cover", models.FloatField()),
                ("precipitation", models.FloatField()),
                ("weather_description", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="MonthlyWeather",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("month_time", models.DateTimeField(auto_now_add=True)),
                ("location", models.CharField(max_length=200)),
                ("average_temperature", models.FloatField()),
                ("average_humidity", models.FloatField()),
                ("average_pressure", models.FloatField()),
                ("average_wind_speed", models.FloatField()),
                ("average_wind_direction", models.FloatField()),
                ("average_cloud_cover", models.FloatField()),
                ("average_precipitation", models.FloatField()),
                ("weather_description", models.CharField(max_length=200)),
            ],
        ),
    ]