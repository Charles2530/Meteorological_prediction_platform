# Generated by Django 5.0.6 on 2024-05-09 11:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("weather", "0004_weatherinfo"),
    ]

    operations = [
        migrations.AddField(
            model_name="dailyweather",
            name="city",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AlterField(
            model_name="dailyweather",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
