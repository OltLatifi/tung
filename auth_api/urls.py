from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("register/", user_register, name="register"),
    path("create-profile/", user_profile, name="create-profile"),
]
