"""Tests for ``user/views.py`` - social login, activation and password reset.

Every view here talks to an external service (Google's tokeninfo endpoint,
Apple's JWKS, or the project's own Djoser API over HTTP), so those network
calls are mocked. The tests then assert how each view reacts to the mocked
response: which auth tokens get issued, which users get created, and which
message is rendered back to the visitor.

Routes exercised:
  - GET  /api/user/gender/             public gender option list
  - GET  /api/user/oauth_token/        Google OAuth state/code -> token exchange
  - POST /api/user/oauth_token_id      Google/Apple id-token -> auth token login
  - POST /api/user/apple_redirect      Apple web callback -> android intent redirect
  - GET  /activate/<uid>/<token>       account activation landing page
  - GET/POST /password_reset/<uid>/<token>  password reset form + submit
"""
import json
from unittest.mock import MagicMock, patch

import pytest
from rest_framework.authtoken.models import Token

from user.models import User

pytestmark = pytest.mark.django_db


def _response(status_code=200, text="", json_data=None):
    """A stand-in for a ``requests``/``httpx`` response object."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = text
    resp.json.return_value = json_data
    return resp


# --- gender list ----------------------------------------------------------

def test_gender_list_is_public(api_client):
    # GenderListView is read-only and open (no authentication required).
    response = api_client.get("/api/user/gender/")

    assert response.status_code == 200
    assert "genders" in response.data


# --- Google OAuth state/code exchange -------------------------------------

def test_oauth_state_code_exchange_returns_token(api_client):
    # The view forwards state+code to the Djoser social endpoint and relays
    # back the token it gets on success.
    with patch("user.views.requests.post") as mock_post:
        mock_post.return_value = _response(200, text=json.dumps({"token": "abc123"}))

        response = api_client.get(
            "/api/user/oauth_token/", {"state": "s", "code": "c"},
        )

    assert response.status_code == 200
    assert response.data == {"token": "abc123"}
    # state + code are passed straight through to the upstream endpoint.
    _, kwargs = mock_post.call_args
    assert kwargs["data"] == {"state": "s", "code": "c"}


def test_oauth_state_code_exchange_relays_upstream_error(api_client):
    # On a non-200 from upstream the view answers 400 with the error text.
    with patch("user.views.requests.post") as mock_post:
        mock_post.return_value = _response(400, text="invalid_grant")

        response = api_client.get(
            "/api/user/oauth_token/", {"state": "s", "code": "c"},
        )

    assert response.status_code == 400
    assert response.data == {"error": "invalid_grant"}


def test_oauth_state_code_non_json_200_is_502(api_client):
    # Upstream replies 200 but with a non-JSON body -> gateway error, not a 500.
    with patch("user.views.requests.post") as mock_post:
        mock_post.return_value = _response(200, text="<html>not json</html>")

        response = api_client.get(
            "/api/user/oauth_token/", {"state": "s", "code": "c"},
        )

    assert response.status_code == 502


def test_oauth_state_code_200_without_token_is_502(api_client):
    # Upstream replies 200 with valid JSON but no "token" key -> gateway error.
    with patch("user.views.requests.post") as mock_post:
        mock_post.return_value = _response(200, text=json.dumps({"detail": "nope"}))

        response = api_client.get(
            "/api/user/oauth_token/", {"state": "s", "code": "c"},
        )

    assert response.status_code == 502


# --- id-token login (Google / Apple) --------------------------------------

GOOGLE_EMAIL = "googler@example.com"
APPLE_EMAIL = "appler@example.com"


def test_google_login_creates_user_and_returns_token(api_client):
    with patch("user.views.requests.get") as mock_get:
        mock_get.return_value = _response(200, json_data={"email": GOOGLE_EMAIL})

        response = api_client.post(
            "/api/user/oauth_token_id", {"token": "id-token", "type": "google"},
        )

    assert response.status_code == 200
    assert response.data["email"] == GOOGLE_EMAIL

    user = User.objects.get(email=GOOGLE_EMAIL)
    assert user.is_active is True
    # The returned auth_token is the user's DRF token.
    assert response.data["auth_token"] == Token.objects.get(user=user).key


def test_login_defaults_to_google_when_type_missing(api_client):
    # No "type" in the payload -> the view assumes Google.
    with patch("user.views.requests.get") as mock_get:
        mock_get.return_value = _response(200, json_data={"email": GOOGLE_EMAIL})

        response = api_client.post("/api/user/oauth_token_id", {"token": "id-token"})

    assert response.status_code == 200
    mock_get.assert_called_once()
    assert User.objects.filter(email=GOOGLE_EMAIL).exists()


def test_google_login_reuses_existing_user_and_token(api_client, make_user):
    existing = make_user(email=GOOGLE_EMAIL)
    token = Token.objects.create(user=existing)

    with patch("user.views.requests.get") as mock_get:
        mock_get.return_value = _response(200, json_data={"email": GOOGLE_EMAIL})

        response = api_client.post(
            "/api/user/oauth_token_id", {"token": "id-token", "type": "google"},
        )

    assert response.status_code == 200
    assert response.data["auth_token"] == token.key
    # No duplicate user was created.
    assert User.objects.filter(email=GOOGLE_EMAIL).count() == 1


def test_apple_login_creates_user_and_returns_token(api_client):
    # The Apple path decodes/validates the JWT instead of calling Google.
    with patch("user.views.decode_and_validate_token") as mock_decode:
        mock_decode.return_value = {"email": APPLE_EMAIL}

        response = api_client.post(
            "/api/user/oauth_token_id", {"token": "apple-jwt", "type": "apple"},
        )

    assert response.status_code == 200
    assert response.data["email"] == APPLE_EMAIL
    mock_decode.assert_called_once_with("apple-jwt")

    user = User.objects.get(email=APPLE_EMAIL)
    assert user.is_active is True
    assert response.data["auth_token"] == Token.objects.get(user=user).key


# --- Apple web -> app redirect --------------------------------------------

def test_apple_redirect_builds_android_intent(client):
    response = client.post(
        "/api/user/apple_redirect",
        data="code=xyz&state=s",
        content_type="application/x-www-form-urlencoded",
    )

    assert response.status_code == 302
    location = response["Location"]
    # The Apple form-post body is wrapped into an android intent:// URL.
    assert location.startswith("intent://callback?code=xyz&state=s")
    assert "package=rainbowchallenge.lt.rainbow_challenge" in location


# --- account activation landing page --------------------------------------

def test_activation_success_message(client):
    with patch("user.views.requests.post") as mock_post:
        mock_post.return_value = _response(204)

        response = client.get("/activate/the-uid/the-token")

    assert response.status_code == 200
    assert "successfully activated" in str(response.context["message"])
    # uid + token are forwarded to the Djoser activation endpoint.
    _, kwargs = mock_post.call_args
    assert kwargs["data"] == {"uid": "the-uid", "token": "the-token"}


def test_activation_failure_message(client):
    with patch("user.views.requests.post") as mock_post:
        mock_post.return_value = _response(400)

        response = client.get("/activate/bad-uid/bad-token")

    assert response.status_code == 200
    assert "can't be activated" in str(response.context["message"])


# --- password reset --------------------------------------------------------

def test_password_reset_get_renders_token_into_context(client):
    # The GET just shows the form, seeding it with the uid/token from the URL
    # so the subsequent POST can submit them.
    response = client.get("/password_reset/the-uid/the-token")

    assert response.status_code == 200
    assert response.context["uid"] == "the-uid"
    assert response.context["token"] == "the-token"


def test_password_reset_post_success(client):
    with patch("user.views.requests.post") as mock_post:
        mock_post.return_value = _response(204)

        response = client.post(
            "/password_reset/the-uid/the-token",
            {
                "uid": "the-uid",
                "token": "the-token",
                "password": "new-pass-123",
                "repeat_password": "new-pass-123",
            },
        )

    assert response.status_code == 200
    assert "changed your password successfully" in str(response.context["message"])
    _, kwargs = mock_post.call_args
    assert kwargs["data"] == {
        "uid": "the-uid",
        "token": "the-token",
        "new_password": "new-pass-123",
        "re_new_password": "new-pass-123",
    }


def test_password_reset_post_failure(client):
    with patch("user.views.requests.post") as mock_post:
        mock_post.return_value = _response(400)

        response = client.post(
            "/password_reset/the-uid/the-token",
            {
                "uid": "the-uid",
                "token": "the-token",
                "password": "new-pass-123",
                "repeat_password": "mismatch",
            },
        )

    assert response.status_code == 200
    assert "something went wrong" in str(response.context["message"])
