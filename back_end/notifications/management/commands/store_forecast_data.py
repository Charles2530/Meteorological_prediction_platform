from django.core.management.base import BaseCommand
from notifications.task import store_catastrophic_forecast_data


class Command(BaseCommand):
    help = 'Store catastrophic forecast data into the database'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        store_catastrophic_forecast_data()
        self.stdout.write(self.style.SUCCESS(
            'Catastrophic forecast data stored successfully'))
