from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register, name="register"),
]