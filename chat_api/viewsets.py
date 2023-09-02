from rest_framework.permissions import IsAuthenticated
from .serializers import server_serializer, channel_serializer, message_serializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from .models import Server, Channel, Messages
from auth_api.models import User
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.db.models import Q

# TODO: Either delete this or delete the method in one of the viewsets and use this method
def mutation_allowed(request, server_id):
    if not server_id:
        return Response({"error": "`server` id not provided in the query params"}, status=status.HTTP_400_BAD_REQUEST)

    # TODO: Refactor this to use an ORM query intead of python comparison
    server_ids = Server.objects.filter(admins=request.user).values_list("id", flat=True)
    server_ids = list(server_ids)
    
    try:
        if int(server_id) not in server_ids:
            return Response({"error": "You are not an admin for the specified server"}, status=status.HTTP_403_FORBIDDEN)
    except ValueError:
        return Response({"error": "`server` should be of type int"}, status=status.HTTP_400_BAD_REQUEST)
    
    return None

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

        # TODO: Refactor this to use an ORM query intead of python comparison
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

        server = get_object_or_404(Server, id=server_id)

        if server.users.filter(pk=request.user.pk).exists() or server.admins.filter(pk=request.user.pk).exists():
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
        # get messages assosciated with the channel
        channel = get_object_or_404(self.model, pk=pk)
        users = list(channel.server.users.all()) + list(channel.server.admins.all())

        if not request.user in users:
            return Response({"error": "You cannot access this channel beacuse you are not part of the server"}, status=status.HTTP_401_UNAUTHORIZED)
        
        messages = Messages.objects.filter(
            channel=pk,
            is_private=False,
        ).order_by("-created_at")

        serializer = message_serializer(messages, many=True)

        return Response({"messages": serializer.data})

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

class message_viewset(viewsets.ViewSet):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    serializer = message_serializer
    model = Messages

    def create(self, request):
        data = request.data.copy()
        data["sender"] = request.user.id

        if request.data.get("receiver") and request.data.get("channel"):
            return Response({"error": "Either `reciever `or `channel` need to be on the request"}, status=status.HTTP_400_BAD_REQUEST)
        elif request.data.get("receiver"):
            data["is_private"] = True
        elif request.data.get("channel"):
            data["is_private"] = False
        
        serializer = self.serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        # the messages beetween two users
        # the messages on a channel is found on the channel viewset
        user_two_id = request.data.get("receiver")

        user_one = request.user
        user_two = get_object_or_404(User, pk=user_two_id)

        messages = self.model.objects.filter(
            is_private=True
        ).filter(
            Q(sender=user_one, receiver=user_two) |
            Q(sender=user_two, receiver=user_one)
        ).order_by("-created_at")

        serializer = self.serializer(messages, many=True)

        return Response({"messages": serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        message = get_object_or_404(self.model, pk=pk)
        updated_body = ""
        
        if message.channel:
            message_server_admins = message.channel.server.admins.all()
            if request.user in message_server_admins:
                updated_body = "Message deleted by admin"

        if request.user == message.sender:
            updated_body = "Message deleted by user"

        if not updated_body:
            return Response({"error": "You don't have permission to delete this message"}, status=status.HTTP_403_FORBIDDEN)

        message.body = updated_body
        message.media = None
        message.save()

        serializer = self.serializer(message)
        return Response({"message": serializer.data}, status=status.HTTP_200_OK)