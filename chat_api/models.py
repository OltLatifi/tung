from django.db import models
from auth_api.models import User
from .helpers import generate_image_directory

class Server(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User)
    # TODO: Maybe a manual m2m relationship is needed to add the admins permissions
    admins = models.ManyToManyField(User, related_name="admins")

class Channel(models.Model):
    name = models.CharField(max_length=255)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)

class Messages(models.Model):
    is_private = models.BooleanField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="receiver")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField()
    media = models.ImageField(upload_to=generate_image_directory)
    created_at = models.DateTimeField(auto_now_add=True)