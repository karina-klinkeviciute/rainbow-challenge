from rest_framework import routers
from django.urls import path, include

from news.views import NewsViewSet

router = routers.DefaultRouter()

app_name = 'news'

router.register(r'news', NewsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
