from rest_framework import mixins, viewsets

from texts.models import Text
from texts.serializers import TextSerializer


class TextViewSet(
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """News API viewets"""
    http_method_names = ('get', 'head', 'options')
    serializer_class = TextSerializer
