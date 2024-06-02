from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


# class RegisterSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(required=True)
#     email = serializers.EmailField(required=True)
#
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'email')
#
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user