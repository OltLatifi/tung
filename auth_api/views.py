from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import user_register_serializer
from .models import User
from rest_framework import status

@api_view(["POST"])
def user_register(request):
    serializer_class = user_register_serializer

    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        