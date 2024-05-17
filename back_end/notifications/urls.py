from django.urls import path
from . import views
from .views import NotificationView


urlpatterns = [
    # path('', views.index, name='index'),
    path('alarm_notices/', views.get_alarm_notice, name='get-alarm-notice'),  # TODO
    path('subscribe/', views.subscribe, name='subscribe'),  # TODO
    path('alarm_notices_brief/', views.get_brief, name='get-brief'),  # TODO
    path('get_alarm_level/', views.get_alarm_level, name='get-alarm-level'),  # TODO
    path('alarm_resent_notices/', views.get_recent, name='get-recent'),  # TODO
    # path('getHazard/', views.getHazard),  # TODO
    # path('getCityInfo/', views.getCityInfo),  # TODO
]
