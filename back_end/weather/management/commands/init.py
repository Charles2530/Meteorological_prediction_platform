from django.core.management.base import BaseCommand
import csv
from weather.models import EarthQuakeInfo, LocationToInfo
from openpyxl import load_workbook
import requests
from bs4 import BeautifulSoup

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--U",
            action="store_true",
            help="Refresh All CityInfo even existed already",
        )
        parser.add_argument(
            "--U",
            action="store_true",
            help="Refresh All CityInfo even existed already",
        )


    # EarthQuakeInfo.objects.all().delete()
    # exit()
    def handle(self, *args, **kwargs):

