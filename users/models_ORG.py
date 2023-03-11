from django.db import models
from django.contrib.auth.models import AbstractUser #For using django user system


# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    #username = None #You can put non if you do not want to username - didnt work
    username = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []