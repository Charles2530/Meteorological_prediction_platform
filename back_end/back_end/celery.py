import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'back_end.settings')

app = Celery('back_end')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_extra()