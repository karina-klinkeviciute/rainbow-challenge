from rest_framework import routers
from django.urls import path, include

from message.views import MessageViewSet
from news.views import NewsViewSet

router = routers.DefaultRouter()

app_name = 'message'

router.register(r'message', MessageViewSet, basename="message")

urlpatterns = [
    path('', include(router.urls)),
]
