from django.views.generic import TemplateView
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from user.models import GenderOptions
from user.serializers import GenderSerializer


class GenderListView(views.APIView):
    http_method_names = ('get', )
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get(self, request, format=None):
        genders = GenderOptions()
        serializer = GenderSerializer(genders)
        return Response(serializer.data)


class UserActivationView(TemplateView):
    """
    This view gets uuid and activation token and then sends to the API endpoint a request to activate
    the user with Djoser. Also displays a nice thank you message.
    """
    template_name = "user/activation.html"

    def get(self, request, *args, **kwargs):
        uid = kwargs.get("uid")
        token = kwargs.get("token")
