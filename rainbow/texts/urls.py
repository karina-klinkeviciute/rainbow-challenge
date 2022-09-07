from rest_framework import routers
from django.urls import path, include

from texts.views import TextViewSet

router = routers.DefaultRouter()

app_name = 'texts'

router.register(r'texts', TextViewSet, basename="texts")

urlpatterns = [
    path('', include(router.urls)),
]
