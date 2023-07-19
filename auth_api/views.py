from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import user_register_serializer, create_user_profile
from rest_framework.response import Response
from rest_framework import status
from .helpers import get_full_user

@api_view(["POST"])
def user_register(request):
    serializer_class = user_register_serializer

    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer_class = create_user_profile

    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        serializer.save()
        profile = get_full_user(serializer.data)
        return Response({"user": profile}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    # return Response({"a":request.user})
