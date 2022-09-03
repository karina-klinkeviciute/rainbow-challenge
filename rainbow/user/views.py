import requests
from django.views.decorators.csrf import requires_csrf_token
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
        url = 'https://rainbowchallenge.lt/auth/users/activation/'
        payload = {'uid': uid, 'token': token}
        response = requests.post(url, data=payload)

        if response.status_code == 204:
            message = _("Congratulations! Your account was successfully activated.")
        else:
            message = _("Sorry, your account can't be activated.")
        context = super().get_context_data(**kwargs)
        context["message"] = message

        return self.render_to_response(context)


class PasswordResetView(TemplateView):
    """
    This view gets uuid and activation token and then sends to the API endpoint a request to activate
    the user with Djoser. Also displays a nice thank you message.
    """
    template_name = "user/password_reset.html"

    def get(self, request, *args, **kwargs):
        # grab the token, render the form, with the token in it
        context = super().get_context_data(**kwargs)
        token = kwargs.get("token")
        uid = kwargs.get("uid")
        context["token"] = token
        context["uid"] = uid

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # get the new password, set it (call api)
        context = super().get_context_data(**kwargs)
        # context["message"] = message
        token = request.POST.get("token")
        uid = request.POST.get("uid")
        password = request.POST.get("password")
        repeat_password = request.POST.get("repeat_password")

        url = 'https://rainbowchallenge.lt/auth/users/reset_password_confirm/'
        print("changing password")
        payload = {'uid': uid, 'token': token, 'new_password': password, 're_new_password': repeat_password}
        response = requests.post(url, data=payload)

        if response.status_code == 204:
            message = _("Congratulations! You changed your password successfully.")
        else:
            message = _("Sorry, something went wrong.")
        context = super().get_context_data(**kwargs)
        context["message"] = message

        return self.render_to_response(context)
