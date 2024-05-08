from rest_framework import serializers

from back_end.models import Books


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'