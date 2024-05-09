# D:/weather/management/commands/fetch_api_data.py
from django.core.management.base import BaseCommand
from celery.schedules import crontab


class Command(BaseCommand):
    help = 'Schedules a task to fetch and save data from an API'

    def handle(self, *args, **kwargs):
        # 每5分钟执行一次任务
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        from django_celery_beat.utils import get_schedule

        if not PeriodicTask.objects.filter(name='fetch_api_data').exists():
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=5,
                period=IntervalSchedule.MINUTES
            )
            periodic_task = PeriodicTask.objects.create(
                crontab=crontab(minute='*/5'),
                task='weather.tasks.fetch_and_save_api_data',
                name='fetch_api_data',
                one_off=False,
                start_time=get_schedule(schedule).datetime,
            )
            self.stdout.write(self.style.SUCCESS(
                'Scheduled fetch_and_save_api_data task to run every 5 minutes'))
        else:
            self.stdout.write(self.style.WARNING('Task already scheduled'))
