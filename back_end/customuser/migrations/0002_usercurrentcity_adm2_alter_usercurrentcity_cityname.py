# Generated by Django 5.0.6 on 2024-06-04 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercurrentcity',
            name='adm2',
            field=models.CharField(default='北京市', max_length=40, verbose_name='二级行政区域名称'),
        ),
        migrations.AlterField(
            model_name='usercurrentcity',
            name='cityName',
            field=models.CharField(default='北京市', max_length=40, verbose_name='当前城市名称'),
        ),
    ]