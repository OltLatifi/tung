from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'server', server_viewset, basename='server')
urlpatterns = router.urls
