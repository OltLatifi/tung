from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Profile(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    about = models.CharField(max_length=511, null=True, blank=True)
    photo = models.ImageField(upload_to='profile/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)