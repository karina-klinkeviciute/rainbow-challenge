from rest_framework import routers
from django.urls import path, include

from news.views import NewsViewSet

router = routers.DefaultRouter()

app_name = 'quiz'

router.register(r'quiz', NewsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
