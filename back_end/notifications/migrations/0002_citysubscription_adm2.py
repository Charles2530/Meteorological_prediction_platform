# Generated by Django 5.0.6 on 2024-06-04 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='citysubscription',
            name='adm2',
            field=models.CharField(default='', max_length=40, verbose_name='二级行政区域名称'),
        ),
    ]