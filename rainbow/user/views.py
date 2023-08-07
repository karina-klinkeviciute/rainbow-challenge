import json

import requests
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, SAFE_METHODS, AllowAny

from user.models import GenderOptions
from user.serializers import GenderSerializer

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
class GenderListView(views.APIView):
    http_method_names = ('get', )
    permission_classes = [ReadOnly, ]

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


class OAuthStateCodeToken(views.APIView):
    http_method_names = ('get',)
    permission_classes = [AllowAny, ]

    def get(self, request, *args, **kwargs):
        state = request.GET.get("state")
        code = request.GET.get("code")
        # todo de-hardcode here
        url = 'https://rainbowchallenge.lt/o/google-oauth2/'
        payload = {'state': state, 'code': code}
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            data = json.loads(response.text)
            token = data["token"]
            content = {"token": token}
            response_status = status.HTTP_200_OK
        else:
            content = {response.text}
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(content, status=response_status)


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
