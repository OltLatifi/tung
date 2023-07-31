from rest_framework import serializers
from auth_api.serializers import user_register_serializer
from .models import Server

class server_serializer(serializers.ModelSerializer):
    admins = user_register_serializer(read_only=True, many=True)
    users = user_register_serializer(read_only=True, many=True)

    class Meta:
        model = Server
        fields = ["name", "admins", "users"]