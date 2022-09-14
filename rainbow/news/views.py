from rest_framework import mixins, viewsets

from news.models import NewsItem
from news.serializers import NewsItemSerializer


class NewsViewSet(
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """News API viewets"""
    http_method_names = ('get', 'head', 'options')
    serializer_class = NewsItemSerializer
    queryset = NewsItem.objects.filter(published=True).order_by('-created_at')
