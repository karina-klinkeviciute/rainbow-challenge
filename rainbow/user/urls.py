from django.urls import path, include
from rest_framework import routers

from user import views

urlpatterns = [
    path('gender/', views.GenderListView.as_view(), name='gender-list'),
]
