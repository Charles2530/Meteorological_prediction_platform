# Generated by Django 5.0.6 on 2024-05-15 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherforecast',
            name='id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]