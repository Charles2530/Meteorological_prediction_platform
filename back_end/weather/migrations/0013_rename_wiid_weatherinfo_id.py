# Generated by Django 5.0.6 on 2024-05-09 16:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("weather", "0012_rename_id_weatherinfo_wiid"),
    ]

    operations = [
        migrations.RenameField(
            model_name="weatherinfo",
            old_name="wiid",
            new_name="id",
        ),
    ]
