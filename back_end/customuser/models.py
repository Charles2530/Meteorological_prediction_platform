from django.contrib.auth.models import User
from django.db import models


class UserAvatar(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="当前用户", default=None)
    avatar = models.CharField(max_length=100, verbose_name="头像URL")

    def __str__(self):
        return f"{self.user.username} - {self.avatar}"

    class Meta:
        verbose_name = "用户头像"
        verbose_name_plural = "用户头像"


class UserCurrentCity(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="当前用户", default=None)
    cityName = models.CharField(max_length=40, verbose_name="当前城市名称", default='北京市')
    adm2 = models.CharField(max_length=40, verbose_name="二级行政区域名称", default='北京市')

    def __str__(self):
        return f"{self.user.username} - {self.cityName}"

    class Meta:
        verbose_name = "用户当前城市"
        verbose_name_plural = "用户当前城市"
