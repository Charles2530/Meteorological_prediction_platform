from django.apps import AppConfig


class BackEndConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'back_end'


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        # 导入并注册模型
        from notifications.models import Notification, WeatherForecast, CitySubscription
