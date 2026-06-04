"""API tests for the message endpoint.

Messages are private to their recipient: a user only sees their own messages
and may mark them as seen (PATCH); creation/deletion are not allowed.
"""
import pytest
from model_bakery import baker

pytestmark = pytest.mark.django_db

MESSAGE_URL = '/api/message/'


def make_message(user, **kwargs):
    return baker.make('message.Message', user=user, **kwargs)


def test_messages_require_authentication(api_client):
    response = api_client.get(MESSAGE_URL)
    assert response.status_code in (401, 403)


def test_user_only_sees_own_messages(auth_client, user, other_user):
    mine = make_message(user)
    make_message(other_user)

    response = auth_client(user).get(MESSAGE_URL)

    assert response.status_code == 200
    assert [item['uuid'] for item in response.data] == [str(mine.uuid)]


def test_user_cannot_retrieve_another_users_message(auth_client, user, other_user):
    theirs = make_message(other_user)

    response = auth_client(user).get(f'{MESSAGE_URL}{theirs.uuid}/')

    assert response.status_code == 404


def test_user_can_mark_own_message_seen(auth_client, user):
    message = make_message(user, seen=False)

    response = auth_client(user).patch(f'{MESSAGE_URL}{message.uuid}/', {'seen': True})

    assert response.status_code == 200
    message.refresh_from_db()
    assert message.seen is True


def test_user_cannot_patch_another_users_message(auth_client, user, other_user):
    theirs = make_message(other_user, seen=False)

    response = auth_client(user).patch(f'{MESSAGE_URL}{theirs.uuid}/', {'seen': True})

    assert response.status_code == 404
    theirs.refresh_from_db()
    assert theirs.seen is False


def test_messages_cannot_be_created_via_api(auth_client, user):
    response = auth_client(user).post(MESSAGE_URL, {'message_text': 'hi'})
    assert response.status_code == 405
