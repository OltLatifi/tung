from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Profile

class user_register_serializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password
        return super().create(validated_data)

class user_profile_serializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"