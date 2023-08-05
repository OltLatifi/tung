from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import server_serializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Server

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def join_server(request, pk):
    server = get_object_or_404(Server, pk=pk)
    if not server.users.filter(pk=request.user.pk).exists():
        server.users.add(request.user)
        serializer = server_serializer(server)
        return Response({"server": serializer.data})
    return Response({"error": "You are already part of this server"}, status=status.HTTP_400_BAD_REQUEST)