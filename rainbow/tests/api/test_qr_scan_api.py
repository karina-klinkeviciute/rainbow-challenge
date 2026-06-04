"""API tests for the QR-code scan endpoint that joins+confirms event challenges."""
import pytest
from model_bakery import baker

from challenge.models.base import ChallengeType
from joined_challenge.models import JoinedChallenge
from joined_challenge.models.base import JoinedChallengeStatus

pytestmark = pytest.mark.django_db

QR_SCAN_URL = '/api/qr_code_scan/'


def make_event_challenge(qr_code, points=15):
    challenge = baker.make(
        'challenge.Challenge', type=ChallengeType.EVENT, published=True,
        points=points, multiple=False, needs_confirmation=False,
    )
    baker.make(
        'challenge.EventParticipantChallenge',
        main_challenge=challenge, qr_code=qr_code, event_name='Pride',
    )
    return challenge


def test_qr_scan_requires_authentication(api_client):
    make_event_challenge('EVENT-1')
    response = api_client.post(QR_SCAN_URL, {'qr_code': 'EVENT-1'})
    assert response.status_code in (401, 403)


def test_qr_scan_joins_and_confirms_the_event_challenge(auth_client, user):
    challenge = make_event_challenge('EVENT-1', points=15)

    response = auth_client(user).post(QR_SCAN_URL, {'qr_code': 'EVENT-1'})

    assert response.status_code == 201
    assert response.data['points'] == 15
    joined = JoinedChallenge.objects.get(user=user, challenge=challenge)
    assert joined.status == JoinedChallengeStatus.CONFIRMED


def test_qr_scan_with_invalid_code_is_rejected(auth_client, user):
    response = auth_client(user).post(QR_SCAN_URL, {'qr_code': 'does-not-exist'})
    assert response.status_code == 400


def test_qr_scan_cannot_complete_same_challenge_twice(auth_client, user):
    make_event_challenge('EVENT-1')
    client = auth_client(user)

    first = client.post(QR_SCAN_URL, {'qr_code': 'EVENT-1'})
    second = client.post(QR_SCAN_URL, {'qr_code': 'EVENT-1'})

    assert first.status_code == 201
    assert second.status_code == 400
