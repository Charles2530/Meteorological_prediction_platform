from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from back_end.models import Books
from back_end.serializer import BooksSerializer


class BooksViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer