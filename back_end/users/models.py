from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserCity(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户名")
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
