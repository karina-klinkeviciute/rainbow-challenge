"""API tests for the djoser-powered authentication flow.

Registration creates an inactive user and sends an activation e-mail; only
after activation can the user obtain a token; the current-user endpoint
requires authentication.
"""
import pytest
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from djoser.utils import encode_uid
from model_bakery import baker

from user.models import User

pytestmark = pytest.mark.django_db

REGISTER_URL = '/auth/users/'
ACTIVATION_URL = '/auth/users/activation/'
LOGIN_URL = '/auth/token/login/'
ME_URL = '/auth/users/me/'

PASSWORD = 'Testpass123!'


def make_login_user(email, is_active):
    user = baker.make('user.User', email=email, is_active=is_active)
    user.set_password(PASSWORD)
    user.save()
    return user


def test_registration_creates_inactive_user_and_sends_activation_email(api_client):
    payload = {'email': 'new@example.com', 'password': PASSWORD, 're_password': PASSWORD}

    response = api_client.post(REGISTER_URL, payload)

    assert response.status_code == 201
    user = User.objects.get(email='new@example.com')
    assert user.is_active is False
    assert len(mail.outbox) == 1


def test_activation_activates_the_user(api_client):
    user = make_login_user('activate@example.com', is_active=False)
    payload = {'uid': encode_uid(user.uid), 'token': default_token_generator.make_token(user)}

    response = api_client.post(ACTIVATION_URL, payload)

    assert response.status_code == 204
    user.refresh_from_db()
    assert user.is_active is True


def test_inactive_user_cannot_obtain_a_token(api_client):
    make_login_user('inactive@example.com', is_active=False)

    response = api_client.post(LOGIN_URL, {'email': 'inactive@example.com', 'password': PASSWORD})

    assert response.status_code == 400


def test_active_user_can_obtain_a_token(api_client):
    make_login_user('active@example.com', is_active=True)

    response = api_client.post(LOGIN_URL, {'email': 'active@example.com', 'password': PASSWORD})

    assert response.status_code == 200
    assert 'auth_token' in response.data


def test_me_requires_authentication(api_client):
    response = api_client.get(ME_URL)
    assert response.status_code in (401, 403)


def test_me_returns_the_current_user(auth_client, user):
    response = auth_client(user).get(ME_URL)

    assert response.status_code == 200
    assert response.data['email'] == user.email
