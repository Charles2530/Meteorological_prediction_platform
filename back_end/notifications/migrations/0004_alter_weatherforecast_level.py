# Generated by Django 5.0.6 on 2024-06-06 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_alter_weatherforecast_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherforecast',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]
