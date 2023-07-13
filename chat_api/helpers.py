def generate_image_directory(instance):
    if not instance.channel_id:
        return "chat/private/"
    return "chat/" + instance.channel.name