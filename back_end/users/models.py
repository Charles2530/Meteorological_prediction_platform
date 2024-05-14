from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    avatar = models.URLField(default="http://dummyimage.com/88x31")
    email = models.EmailField(max_length=100, blank=True, null=True)
    currentCityName = models.CharField(max_length=40, default='北京市')
    role = models.IntegerField(default=1)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户画像"
        verbose_name_plural = "用户画像"
