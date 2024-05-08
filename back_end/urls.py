from django.urls import path, include
from rest_framework.routers import DefaultRouter

from back_end import views


router = DefaultRouter()
router.register('back_end', views.BooksViewSet)

urlpatterns = [
    path('', include(router.urls)),
]