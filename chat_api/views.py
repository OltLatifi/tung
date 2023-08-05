from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import server_serializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Server
from auth_api.models import User

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def join_server(request, pk):
    server = get_object_or_404(Server, pk=pk)
    if not server.users.filter(pk=request.user.pk).exists():
        server.users.add(request.user)
        serializer = server_serializer(server)
        return Response({"server": serializer.data})
    return Response({"error": "You are already part of this server"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_admin(request, pk):
    server = get_object_or_404(Server, pk=pk)

    user_id = request.data.get("user")

    if not user_id:
        return Response({"error": "`user` needs to be specified"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user_id = int(user_id)
    except ValueError:
        return Response({"error": "`user` should be of type int"}, status=status.HTTP_400_BAD_REQUEST)

    if not server.admins.filter(pk=request.user.pk).exists():
        return Response({"error": "You are not authorized to add an admin"}, status=status.HTTP_403_FORBIDDEN)
    
    user = get_object_or_404(User, pk=user_id)
    if not server.admins.filter(pk=user_id).exists():
        server.admins.add(user)
        serializer = server_serializer(server)
        return Response({"server": serializer.data})
    return Response({"error": "You are already an admin of this server"}, status=status.HTTP_400_BAD_REQUEST)