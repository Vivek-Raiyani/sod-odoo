from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('details/', details, name="details"),
    path('details/<int:item_id>/', details, name='item_details'),
    path('additem/', create_item, name="additem"),
    path("dashboard/", dashboard, name="dashboard"),
    path("admindashboard/", admindashboard, name="admindashboard")
]