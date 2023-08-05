from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'server', server_viewset, basename='server')
router.register(r'channel', channel_viewset, basename='channel')
urlpatterns = router.urls
