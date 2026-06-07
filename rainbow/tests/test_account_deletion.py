"""Tests for account deletion.

There is a single account-deletion path through the API: djoser's
``DELETE /auth/users/me/``, which requires authentication and the user's
current password. It is a *soft* delete: the account is flagged
(``marked_for_deletion``) and admins are notified, but the row is kept so an
admin can process it. The old, unauthenticated ``/delete_account`` HTML view
has been removed (it let anyone delete any account by e-mail).
"""
import pytest
from django.core import mail
from model_bakery import baker
from rest_framework.test import APIClient

from user.models import User

pytestmark = pytest.mark.django_db

LEGACY_DELETE_URL = '/delete_account'
ME_URL = '/auth/users/me/'
PASSWORD = 'Testpass123!'


def make_user_with_password(email, **kwargs):
    user = baker.make('user.User', email=email, is_active=True, **kwargs)
    user.set_password(PASSWORD)
    user.save()
    return user


def test_legacy_delete_account_endpoint_is_removed():
    response = APIClient().post(LEGACY_DELETE_URL, {'email': 'someone@example.com'})
    assert response.status_code == 404


def test_account_deletion_requires_authentication():
    response = APIClient().delete(ME_URL, {'current_password': PASSWORD}, format='json')
    assert response.status_code in (401, 403)


def test_deleting_own_account_soft_deletes_and_notifies_admins():
    make_user_with_password('admin@example.com', is_admin=True)  # recipient of the notice
    user = make_user_with_password('owner@example.com')
    client = APIClient()
    client.force_authenticate(user)

    response = client.delete(ME_URL, {'current_password': PASSWORD}, format='json')

    assert response.status_code == 204
    user.refresh_from_db()
    # Row is kept but flagged for an admin to process.
    assert user.marked_for_deletion is True
    assert user.marked_for_deletion_date is not None
    assert len(mail.outbox) == 1


def test_account_deletion_with_wrong_password_is_rejected():
    user = make_user_with_password('owner@example.com')
    client = APIClient()
    client.force_authenticate(user)

    response = client.delete(ME_URL, {'current_password': 'WrongPass1!'}, format='json')

    assert response.status_code == 400
    user.refresh_from_db()
    assert user.marked_for_deletion is False


def test_soft_delete_marks_but_keeps_the_account(user):
    user.soft_delete()

    user.refresh_from_db()
    assert user.marked_for_deletion is True
    assert user.marked_for_deletion_date is not None


def test_hard_delete_still_removes_the_row(user):
    # delete() is left as Django's normal hard delete so admins can still
    # remove users via the Django admin.
    pk = user.pk
    user.delete()

    assert not User.objects.filter(pk=pk).exists()
