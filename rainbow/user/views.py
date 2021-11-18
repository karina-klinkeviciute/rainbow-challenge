import requests
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
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
        # todo de-hardcode here
        url = "https://rainbowchallenge.lt/api/v1/auth/users/activation/"
        payload = {'uid': uid, 'token': token}
        response = requests.post(url, data=payload)

        if response.status_code == 204:
            message = _("Sorry, your account can't be activated.")
        else:
            message = _("Congratulations! Your account was successfully activated.")
        context = super().get_context_data(**kwargs)
        context["message"] = message

        return self.render_to_response(context)
