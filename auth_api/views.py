from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import user_register_serializer, user_profile_serializer
from rest_framework.response import Response
from rest_framework import status
from .helpers import get_full_user
from .models import Profile
from django.shortcuts import get_object_or_404

@api_view(["POST"])
def user_register(request):
    serializer_class = user_register_serializer

    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST", "PATCH"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer_class = user_profile_serializer
    request.data["user"] = request.user.id

    if request.method == "POST":
        serializer = serializer_class(data=request.data)
    elif request.method == "PATCH":
        profile = get_object_or_404(Profile, user=request.data["user"])        
        serializer = serializer_class(profile, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        profile = get_full_user(serializer.data)
        return Response({"user": profile}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
