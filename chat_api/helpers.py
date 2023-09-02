from rest_framework.response import Response
from rest_framework import status

def generate_image_directory(instance, filename):
    if not instance.channel_id:
        return "chat/private/" + filename
    return f"chat/{instance.channel.name}-{instance.channel.server_id}/{filename}"

def allow_server_mutation(request, server, user_id):
    if not user_id:
        return Response({"error": "`user` needs to be specified"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user_id = int(user_id)
    except ValueError:
        return Response({"error": "`user` should be of type int"}, status=status.HTTP_400_BAD_REQUEST)

    if not server.admins.filter(pk=request.user.pk).exists():
        return Response({"error": "You are not authorized to complete this action"}, status=status.HTTP_403_FORBIDDEN)
    
    return None