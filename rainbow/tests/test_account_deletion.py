"""Tests for account deletion.

There is a single account-deletion path through the API: djoser's
``DELETE /auth/users/me/``, which requires authentication and the user's
current password. The old, unauthenticated ``/delete_account`` HTML view has
been removed (it let anyone delete any account by e-mail).
"""
import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from user.models import User

pytestmark = pytest.mark.django_db

LEGACY_DELETE_URL = '/delete_account'
ME_URL = '/auth/users/me/'
PASSWORD = 'Testpass123!'


def make_user_with_password(email):
    user = baker.make('user.User', email=email, is_active=True)
    user.set_password(PASSWORD)
    user.save()
    return user


def test_legacy_delete_account_endpoint_is_removed():
    response = APIClient().post(LEGACY_DELETE_URL, {'email': 'someone@example.com'})
    assert response.status_code == 404


def test_account_deletion_requires_authentication():
    response = APIClient().delete(ME_URL, {'current_password': PASSWORD}, format='json')
    assert response.status_code in (401, 403)


def test_user_can_delete_own_account_with_correct_password():
    user = make_user_with_password('owner@example.com')
    client = APIClient()
    client.force_authenticate(user)

    response = client.delete(ME_URL, {'current_password': PASSWORD}, format='json')

    assert response.status_code == 204
    assert not User.objects.filter(pk=user.pk).exists()


def test_account_deletion_with_wrong_password_is_rejected():
    user = make_user_with_password('owner@example.com')
    client = APIClient()
    client.force_authenticate(user)

    response = client.delete(ME_URL, {'current_password': 'WrongPass1!'}, format='json')

    assert response.status_code == 400
    assert User.objects.filter(pk=user.pk).exists()
