from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    about = models.CharField(max_length=511)
    photo = models.ImageField(upload_to='profile/')

class User(AbstractUser):
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)