from django.urls import path
from .views import *

urlpatterns = [
    path("register/", user_register, name="register"),
    path("profile/", user_profile, name="profile"),
]
