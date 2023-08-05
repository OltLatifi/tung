from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import server_serializer, channel_serializer
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Server, Channel, Messages
from django.forms import model_to_dict

class server_viewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer = server_serializer
    model = Server

    def list(self, request):
        # TODO: Add Pagination
        queryset = self.model.objects.filter(Q(users=request.user) | Q(admins=request.user))
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
        queryset = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer(queryset)
        return Response({"server": serializer.data})

    def partial_update(self, request, pk=None):
        queryset = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer(queryset, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"server": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer(queryset)
        server_data = serializer.data

        queryset.delete()
        return Response({"server": server_data})


class channel_viewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer = channel_serializer
    model = Channel

    def mutation_allowed(self, request, server_id):
        if not server_id:
            return Response({"error": "`server` id not provided in the query params"}, status=status.HTTP_400_BAD_REQUEST)

        server_ids = Server.objects.filter(admins=request.user).values_list("id", flat=True)
        server_ids = list(server_ids)
        
        try:
            if int(server_id) not in server_ids:
                return Response({"error": "You are not an admin for the specified server"}, status=status.HTTP_403_FORBIDDEN)
        except ValueError:
            return Response({"error": "`server` should be of type int"}, status=status.HTTP_400_BAD_REQUEST)
        
        return None

    def list(self, request):
        server_id = request.GET.get("server")

        if not server_id:
            return Response({"error": "`server` id not provided in the query params"}, status=status.HTTP_400_BAD_REQUEST)

        server = Server.objects.get(id=server_id)

        if request.user in server.users.all() or request.user in server.admins.all():
            queryset = self.model.objects.filter(
                server=server
            )
            serializer = self.serializer(queryset, many=True)
            return Response({"channels": serializer.data})
        else:
            return Response({"error": "You don't have access to the specified server"}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        server_id = request.GET.get("server")

        response = self.mutation_allowed(request, server_id)
        if response is not None:
            return response
    
        request.data["server"] = server_id
        serializer = self.serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"channel": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        server_id = request.GET.get("server")

        response = self.mutation_allowed(request, server_id)
        if response is not None:
            return response
        
        # get messages assosciated with the channel
        messages = Messages.objects.filter(
            channel=pk,
            is_private=False,
        ).order_by("created_at")

        # TODO: When the message serializer is ready continue this method
        # TODO: Decide if pinned messages should be done in a seperate view
        # TODO: Add pagination with backwards infinite scroll

    def partial_update(self, request, pk=None):
        server_id = request.GET.get("server")

        response = self.mutation_allowed(request, server_id)
        if response is not None:
            return response
    
        queryset = get_object_or_404(self.model, pk=pk)

        if not queryset.server.id == int(server_id):
            return Response({"error": "You cannot delete a channel present in another server"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.serializer(queryset, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"channel": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        server_id = request.GET.get("server")

        response = self.mutation_allowed(request, server_id)
        if response is not None:
            return response
    
        queryset = get_object_or_404(self.model, pk=pk)

        if not queryset.server.id == int(server_id):
            return Response({"error": "You cannot delete a channel present in another server"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.serializer(queryset)
        channel_data = serializer.data

        queryset.delete()
        return Response({"server": channel_data})