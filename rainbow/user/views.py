import json

import logging
import uuid
from datetime import datetime

import httpx
import requests

import jwt
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import TemplateView, FormView
from django.utils.translation import gettext_lazy as _

from rest_framework import views, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, SAFE_METHODS, AllowAny

from user.forms import AccountDeletionForm
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
    try:
        decoded_jwt = jwt.decode(token, key, [header["alg"]], audience="org.rainbowchallenge")
    except:
        decoded_jwt = jwt.decode(token, key, [header["alg"]], audience="rainbow_challenge")
    return decoded_jwt

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
        token = request.data.get("token")
        token_type = request.data.get("type")
        print("TYPE: ", token_type)
        if token_type is None:
            token_type = "google"

        #     for testing only
        # type = "apple"
        # token = """eyJraWQiOiJmaDZCczhDIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJodHRwczovL2FwcGxlaWQuYXBwbGUuY29tIiwiYXVkIjoib3JnLnJhaW5ib3djaGFsbGVuZ2UiLCJleHAiOjE3MDYwMzMyMjYsImlhdCI6MTcwNTk0NjgyNiwic3ViIjoiMDAxNjQ3LjY0YTNlNWNmM2Y1OTQ2YTViMjdlNmFjZWQwNDU3MzVkLjE1MjciLCJjX2hhc2giOiJoVmJWMmxNdXZPVXJyS1gtN2dLTXVBIiwiZW1haWwiOiJhcGFiaXRhc2RldjFAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOiJ0cnVlIiwiYXV0aF90aW1lIjoxNzA1OTQ2ODI2LCJub25jZV9zdXBwb3J0ZWQiOnRydWV9.ZaWQzN4VywDtn2lq7_K5ITAVbUkO9mo7UVAWItpxj3dDgx94BM493KyCNkyGVEyoCpZmZl7VisTIxWAKksgti1TCx3u-2Jvxt6XEhUprmHIuCZAiVJMEZejvaV5E2_Yt5i6l7bpkQu_UPYWdPhpNdDjk8pVmd-iPbC4sooacIf8uyUslyBfArdaP8EhQkHUTNAnKZh1smQa-xWZ4r01G_PpQX4WzbVLkdasu7Q3Gg5yj_1N8RbmJo3QxwZnK8qXjnZW9OYGolSeeNQIQE_DAn4lirO--bh6ElchLUX_hh2mLhGppKyhTapxunw_m3w6XjcZ_BKfQ5wDn7NiSXL5Z8g"""

        if token_type == "google":

            response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")

            print("RESPONSE:", response.text)

            userid = response.json()["email"]

        if token_type == "apple":

            user_data = decode_and_validate_token(token)

            logger.info("RESPONSE APPLE: ", user_data)

            userid = user_data["email"]

            print(user_data)

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

class HttpResponseRedirectIntent(HttpResponseRedirect):
    allowed_schemes = ['http', 'https', 'ftp', 'intent']

@csrf_exempt
def apple_redirect(request):
    package = 'rainbowchallenge.lt.rainbow_challenge'
    payload = request.body.decode('utf-8')
    logger.info(f"REQUEST BODY: {request.body}")
    logger.info(f"REQUEST POST: {request.POST}")
    to = f"intent://callback?{payload}#Intent;package={package};scheme=signinwithapple;end"
    logger.info(to)
    return HttpResponseRedirectIntent(to)
    # redirect_intent(f"intent://callback?{payload}#Intent;package={package};scheme=signinwithapple;end")

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


class DeleteAccountView(FormView):
    template_name = "user/deletion.html"
    form_class = AccountDeletionForm
    success_url = "/"

    def form_valid(self, form):
        user = User.objects.get(email=form.cleaned_data["email"])
        user.marked_for_deletion = True
        user.marked_for_deletion_date = datetime.now()
        user.save()
        return super().form_valid(form)
