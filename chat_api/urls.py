from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *
from .viewsets import *

router = DefaultRouter()
router.register(r'server', server_viewset, basename='server')
router.register(r'channel', channel_viewset, basename='channel')

urlpatterns = [
    path("server/<int:pk>/join", join_server, name="join-server"),
    path("server/<int:pk>/promote", add_admin, name="add-admin"),
]

urlpatterns += router.urls
