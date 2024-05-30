from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class ProfileManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Profile(AbstractUser):
    avatar = models.URLField(default="http://dummyimage.com/88x31")
    email = models.EmailField(max_length=100, blank=True, default='')
    currentCityName = models.CharField(max_length=40, default='北京市')
    role = models.IntegerField(default=1)

    objects = ProfileManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户画像"
        verbose_name_plural = "用户画像"


class UserCurrentCity(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name="当前用户", default=None)
    cityName = models.CharField(max_length=40, verbose_name="当前城市名称")

    def __str__(self):
        return f"{self.profile.username} - {self.cityName}"

    class Meta:
        verbose_name = "用户当前城市"
        verbose_name_plural = "用户当前城市"
