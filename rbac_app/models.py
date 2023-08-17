from django.db import models
from django.contrib.postgres.fields import JSONField
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.postgres.fields import ArrayField


class User(models.Model):
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    mobile = models.BigIntegerField(unique=True)
    role = models.CharField(max_length=10,default="user")
    tokens = models.JSONField(max_length=350,null=True)

    def __str__(self):
        return f"{self.username}"

class API(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    endpoint = models.CharField(max_length=100)
    method = models.CharField(max_length=10)
    mapped_users = ArrayField(models.IntegerField(null=True,blank=True))

    def __str__(self):
        return f"{self.name}"    