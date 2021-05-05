from django.urls import path, include
from rest_framework import routers

from user import views

urlpatterns = [
    path('gender/', views.GenderListView.as_view(), name='gender-list'),
    path('<user_uuid>/prize', views.UserClaimedPrizeAPIView.as_view(), name='user-prize-list')
]
