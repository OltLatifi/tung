from django.db import models
from auth_api.models import User
from .helpers import generate_image_directory

class Server(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User)
    admins = models.ManyToManyField(User, related_name="admins")

class Channel(models.Model):
    name = models.CharField(max_length=255)
    server_id = models.ForeignKey(Server, on_delete=models.CASCADE)

class Messages(models.Model):
    is_private = models.BooleanField()
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="receiver")
    channel_id = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField()
    media = models.ImageField(upload_to=generate_image_directory)