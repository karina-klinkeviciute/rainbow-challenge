"""Regression tests for DeleteAccountView authorization.

The view is a session-authenticated HTML form, so it is driven with Django's
test client. A user may only delete their *own* account: anonymous requests and
attempts to delete someone else's account by e-mail must not delete anything.
"""
import pytest
from django.test import Client

from user.models import User

pytestmark = pytest.mark.django_db

DELETE_URL = '/delete_account'


def test_anonymous_user_cannot_delete_an_account(user):
    response = Client().post(DELETE_URL, {'email': user.email})

    # LoginRequiredMixin redirects to the login page instead of deleting.
    assert response.status_code in (302, 403)
    assert User.objects.filter(pk=user.pk).exists()


def test_user_can_delete_their_own_account(user):
    client = Client()
    client.force_login(user)

    response = client.post(DELETE_URL, {'email': user.email})

    assert response.status_code == 302
    assert not User.objects.filter(pk=user.pk).exists()


def test_user_cannot_delete_another_users_account(user, other_user):
    client = Client()
    client.force_login(user)

    client.post(DELETE_URL, {'email': other_user.email})

    # Neither the targeted account nor the requester's own account is deleted.
    assert User.objects.filter(pk=other_user.pk).exists()
    assert User.objects.filter(pk=user.pk).exists()
