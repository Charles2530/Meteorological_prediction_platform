from django.db import models
from datetime import datetime

class Notification(models.Model):
    pubTime = models.DateTimeField(default=datetime.now)
    place = models.CharField(max_length=100, default="")
    type = models.CharField(max_length=50, default="")
    time = models.DateTimeField()
    level = models.CharField(max_length=10, default="")