from rest_framework import serializers
from auth_api.serializers import user_register_serializer
from .models import Server, Channel, Messages

class server_serializer(serializers.ModelSerializer):
    admins = user_register_serializer(read_only=True, many=True)
    users = user_register_serializer(read_only=True, many=True)

    class Meta:
        model = Server
        fields = ["id" ,"name", "admins", "users"]

class channel_serializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ["id", "name", "server"]

class message_serializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = "__all__"

    def create(self, validated_data):
        image_data = validated_data.pop('media', None)
        instance = self.Meta.model.objects.create(**validated_data)
        
        if image_data:
            instance.media = image_data
            instance.save()
        
        return instance