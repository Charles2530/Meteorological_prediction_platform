# Generated by Django 5.0.6 on 2024-06-05 16:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0010_weatherinfo_winddir_alter_weatherinfo_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyweather',
            name='fxDate',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
