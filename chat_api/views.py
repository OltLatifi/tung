from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import server_serializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Server
from auth_api.models import User
from .helpers import allow_server_mutation

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
    user_id = request.data.get("user")
    server = get_object_or_404(Server, pk=pk)

    response = allow_server_mutation(request, server, user_id)
    if response is not None:
        return response
    
    user = get_object_or_404(User, pk=user_id)
    if not server.admins.filter(pk=user_id).exists():
        server.admins.add(user)
        serializer = server_serializer(server)
        return Response({"server": serializer.data})
    return Response({"error": "You are already an admin of this server"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove_user(request, pk):
    user_id = request.data.get("user")
    server = get_object_or_404(Server, pk=pk)

    response = allow_server_mutation(request, server, user_id)
    if response is not None:
        return response
    
    user = get_object_or_404(User, pk=user_id)
    if server.users.filter(pk=user_id).exists():
        server.users.remove(user)
        serializer = server_serializer(server)
        return Response({"server": serializer.data})
    return Response({"error": "The user specified is not part of the server"}, status=status.HTTP_400_BAD_REQUEST)