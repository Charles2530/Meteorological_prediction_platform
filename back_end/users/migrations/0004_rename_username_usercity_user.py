# Generated by Django 5.0.6 on 2024-05-09 15:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="usercity",
            old_name="username",
            new_name="user",
        ),
    ]