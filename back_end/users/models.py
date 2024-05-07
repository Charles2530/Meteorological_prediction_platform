from django.db import models


# Create your models here.
# class UserManager(models.Manager):
#     def create_user(self, username, avatar, email, password, role, last_login):
#         user = self.create(username=username, avatar=avatar, email=email, password=password, role=role, last_login=last_login)
#         return user


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
