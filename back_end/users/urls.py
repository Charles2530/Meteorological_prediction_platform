from django.urls import path
from . import views
# from django_cron import cron
# from .views import RegisterView


urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),

    path('manage/user/list', views.user_list, name='user_list'),
    path('manage/user/delete', views.delete_user, name='delete_user'),
    path('manage/user/email', views.update_user_email, name='change_email'),
    path('manage/user/password', views.update_user_password, name='change_password'),

    path('login/', views.my_login, name='login'),
    path('register/', views.my_register, name='register'),

    path('get_info/', views.user_info, name='get_info'),

    path('operate/email/', views.update_user_email, name='update_email'),
    path('operate/password/', views.update_user_password, name='change_password'),
]
