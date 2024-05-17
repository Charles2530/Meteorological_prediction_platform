from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    avatar = models.URLField(blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, default='北京市')
    role = models.IntegerField(default=1)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户画像"
        verbose_name_plural = "用户画像"


class UserCity(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="用户名")
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} - {self.city}"

    class Meta:
        verbose_name = "用户城市"
        verbose_name_plural = "用户城市"



# class User(models.Model):
#     uid = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=100)
#     avatar = models.URLField()
#     email = models.EmailField(max_length=100, blank=True, null=True)
#     password = models.CharField(max_length=100)
#     role = models.IntegerField()
#     last_login = models.DateTimeField()

#     def __str__(self):
#         return self.username
