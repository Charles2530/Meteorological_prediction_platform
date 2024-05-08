from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Notification
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NotificationSerializer

# Create your views here.


class NotificationView(APIView):
    def get(self, request, format=None):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


def get_alarm_notice(request):
    pass


@require_http_methods(['POST'])
def subscribe(request):
    pass


@require_http_methods(['GET'])
def subscribe(request):
    pass


def get_brief(request):
    pass


def get_alarm_level(request):
    pass


def get_recent(request):
    pass