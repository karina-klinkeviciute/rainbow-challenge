from rest_framework import mixins, viewsets

from message.models import Message
from message.serializers import MessageSerializer


class MessageViewSet(
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet):
    """News API viewets"""
    http_method_names = ('get', 'patch', 'head', 'options')
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user).order_by("-time_sent")
