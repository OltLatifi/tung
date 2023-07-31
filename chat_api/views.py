from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import server_serializer
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Server


class server_viewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer = server_serializer

    def list(self, request):
        queryset = Server.objects.filter(Q(users=request.user) | Q(admins=request.user))
        serializer = self.serializer(queryset, many=True)
        return Response({"servers": serializer.data})

    def create(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            server = serializer.save()
            server.admins.add(request.user)
            return Response({"server": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Server, pk=pk)
        serializer = self.serializer(queryset)
        return Response({"server": serializer.data})

    def partial_update(self, request, pk=None):
        queryset = get_object_or_404(Server, pk=pk)
        serializer = self.serializer(queryset, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"server": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = get_object_or_404(Server, pk=pk)
        serializer = self.serializer(queryset)
        server_data = serializer.data

        queryset.delete()
        return Response({"server": server_data})