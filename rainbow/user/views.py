import json

import logging
import uuid

import httpx
import requests

import jwt

from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from rest_framework import views, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, SAFE_METHODS, AllowAny

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from user.models import GenderOptions, User
from user.serializers import GenderSerializer

logger = logging.getLogger('root')

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
        logger.info(request.headers)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if "Cookie" in request.headers:
            cookie = request.headers["Cookie"]
            headers["Cookie"] = cookie
        state = request.GET.get("state")
        code = request.GET.get("code")
        # todo de-hardcode here
        url = 'https://rainbowchallenge.lt/auth/o/google-oauth2/'
        payload = {'state': state, 'code': code}


        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            data = json.loads(response.text)
            token = data["token"]
            content = {"token": token}
            response_status = status.HTTP_200_OK
        else:
            content = {response.text}
            response_status = status.HTTP_400_BAD_REQUEST

        return Response(content, status=response_status)


def decode_access_token(authorisation_token):
    # get public key from jwks uri
    response = httpx.get(url="https://appleid.apple.com/auth/keys")

    # gives the set of jwks keys.the keys has to be passed as it is to jwt.decode() for signature verification.
    key = response.json()
    print(key)

    # get the algorithm type from the request header
    algorithm = jwt.get_unverified_header(authorisation_token).get('alg')

    user_info = jwt.decode(authorisation_token, key, algorithms=algorithm)

    return user_info

# šitas, atrodo, veikia
def decode_and_validate_token(token):
    unvalidated = jwt.decode(token, options={"verify_signature": False})
    jwks_url = "https://appleid.apple.com/auth/keys"
    jwks_client = jwt.PyJWKClient(jwks_url)
    header = jwt.get_unverified_header(token)
    key = jwks_client.get_signing_key(header["kid"]).key
    return jwt.decode(token, key, [header["alg"]])

# Another option:
def decode_jwt_token(token: str, auth_domain: str, audience: str):
    jwks_url = f'https://{auth_domain}/.well-known/jwks.json'
    jwks_client = jwt.PyJWKClient(jwks_url)
    header = jwt.get_unverified_header(token)
    key = jwks_client.get_signing_key(header["kid"]).key
    decoded = jwt.decode(token, key, [header["alg"]], audience=audience)
    return decoded



class OAuthTokenID(views.APIView):
    http_method_names = ('post', 'head', 'options')
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        token = request.POST.get("token")
        type = request.POST.get("type")
        if type is None:
            type = "google"

        #     for testing only
        # type = "apple"
        # token = """eyJraWQiOiJsVkhkT3g4bHRSIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJodHRwczovL2FwcGxlaWQuYXBwbGUuY29tIiwiYXVkIjoib3JnLnJhaW5ib3djaGFsbGVuZ2UiLCJleHAiOjE3MDU2Njk5MDUsImlhdCI6MTcwNTU4MzUwNSwic3ViIjoiMDAxNjQ3LjY0YTNlNWNmM2Y1OTQ2YTViMjdlNmFjZWQwNDU3MzVkLjE1MjciLCJjX2hhc2giOiJDQ2RITGpBQW1iOEdXamlFU2VOdkRnIiwiZW1haWwiOiJhcGFiaXRhc2RldjFAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOiJ0cnVlIiwiYXV0aF90aW1lIjoxNzA1NTgzNTA1LCJub25jZV9zdXBwb3J0ZWQiOnRydWV9.XI5_20oHzg-az708bJeBZOeRd3eozG96IYk2Q0HWqei1GCYGm_KDYThpRKg7T_kwXOEOjRJ_Blx7gjLmKhgWSVpBqOVaSFreoCiVNFRUBkbiZBoYeCJpSICh1ZOqq2_HpPZJTQN3R9xWvXYMAEls7zP_6lGSqLpC2FndijI7V_DAYB3hVFFIpRp_D9nnWOx2B6GRxD2jTato7qZ1mv2zEA0j5xRH5u0OcKxbb5hs9zxev1EiT9GYGWqX-pKopHvgtzOvSdAglygN9oAyoMpbQD-TEbu1-XzfwmdNcwi4QjMD4YGT5yfhRJr1My5j7WYm1Y4VVOSnSNkDtiaiLBKzWA"""

        if type == "google":

            response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")

            print("RESPONSE:", response.text)

            userid = response.json()["email"]

        if type == "apple":

            user_data = decode_and_validate_token(token)

            print("RESPONSE APPLE: ", user_data)

            userid = user_data["email"]

        try:
            # id_info = id_token.verify_oauth2_token(token, google_requests.Request())
            # userid = id_info['sub']


            # userid = "karina.klinkeviciute@gmail.com"

            # user_token = settings.TOKEN_MODEL.objects.get()
            try:
                user = User.objects.get(email=userid)
            except User.DoesNotExist:
                user = User.objects.create_user(userid, str(uuid.uuid4()))

            try:
                user_token = Token.objects.get(user=user).key
            except Token.DoesNotExist:
                user_token = Token.objects.create(user=user).key

            user.is_active = True
            user.save()

            return Response(data={"auth_token": user_token, "email": userid})

        except ValueError:
            raise PermissionDenied({"message": "Wrong credentials"})


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
