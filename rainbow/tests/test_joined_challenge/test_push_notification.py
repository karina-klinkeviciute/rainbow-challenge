"""Tests for the push notification sent when a challenge is confirmed.

Nothing else exercises the fcm-django/firebase-admin path, and its API is the
one most likely to shift under a library upgrade, so this pins down what the
app hands to the device: a ``firebase_admin.messaging.Message`` carrying the
"challenge_confirmed" category.
"""
import pytest
from firebase_admin.messaging import Message

from fcm_django.models import FCMDevice
from joined_challenge.models.base import JoinedChallengeStatus

pytestmark = pytest.mark.django_db


@pytest.fixture
def sent_messages(monkeypatch):
    """Collect what would be sent, instead of talking to Firebase."""
    sent = []
    monkeypatch.setattr(
        FCMDevice, "send_message", lambda self, message, *a, **kw: sent.append(message)
    )
    return sent


def test_confirming_a_challenge_pushes_to_the_users_devices(
    user, make_challenge, make_joined_challenge, sent_messages,
):
    FCMDevice.objects.create(user=user, registration_id="token-1", active=True)
    challenge = make_challenge(needs_confirmation=True, points=15)
    joined = make_joined_challenge(user, challenge=challenge)

    joined.status = JoinedChallengeStatus.CONFIRMED
    joined.save()

    assert len(sent_messages) == 1
    message = sent_messages[0]
    assert isinstance(message, Message)
    assert message.data == {"category": "challenge_confirmed"}
    assert "15" in message.notification.body


def test_no_push_when_the_challenge_needs_no_confirmation(
    user, make_challenge, make_joined_challenge, sent_messages,
):
    FCMDevice.objects.create(user=user, registration_id="token-2", active=True)
    challenge = make_challenge(needs_confirmation=False)
    joined = make_joined_challenge(user, challenge=challenge)

    joined.status = JoinedChallengeStatus.CONFIRMED
    joined.save()

    assert sent_messages == []
