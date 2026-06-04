"""API tests for the join / complete write flow on joined challenges.

Uses the Article challenge type as a representative of the shared
``BaseJoinedChallengeSerializer`` create/update behaviour.
"""
import pytest
from model_bakery import baker

from challenge.models.base import ChallengeType
from joined_challenge.models import JoinedChallenge, ArticleJoinedChallenge
from joined_challenge.models.base import JoinedChallengeStatus

pytestmark = pytest.mark.django_db

ARTICLE_JOINED_URL = '/api/joined_challenge/article_joined_challenge/'


def make_challenge(multiple=True, needs_confirmation=False):
    challenge = baker.make(
        'challenge.Challenge',
        type=ChallengeType.ARTICLE,
        published=True,
        points=10,
        multiple=multiple,
        needs_confirmation=needs_confirmation,
    )
    baker.make('challenge.ArticleChallenge', main_challenge=challenge)
    return challenge


def test_joining_requires_authentication(api_client):
    challenge = make_challenge()
    payload = {'main_joined_challenge': {'challenge': str(challenge.uuid)}}

    response = api_client.post(ARTICLE_JOINED_URL, payload, format='json')

    assert response.status_code in (401, 403)


def test_user_can_join_a_challenge(auth_client, user):
    challenge = make_challenge()
    payload = {'main_joined_challenge': {'challenge': str(challenge.uuid)}}

    response = auth_client(user).post(ARTICLE_JOINED_URL, payload, format='json')

    assert response.status_code == 201
    joined = JoinedChallenge.objects.get(user=user, challenge=challenge)
    assert joined.status == JoinedChallengeStatus.JOINED
    assert ArticleJoinedChallenge.objects.filter(main_joined_challenge=joined).exists()


def test_non_multiple_challenge_can_only_be_joined_once(auth_client, user):
    challenge = make_challenge(multiple=False)
    client = auth_client(user)
    payload = {'main_joined_challenge': {'challenge': str(challenge.uuid)}}

    first = client.post(ARTICLE_JOINED_URL, payload, format='json')
    second = client.post(ARTICLE_JOINED_URL, payload, format='json')

    assert first.status_code == 201
    assert second.status_code == 400
    assert JoinedChallenge.objects.filter(user=user, challenge=challenge).count() == 1


def test_completing_a_challenge_that_needs_no_confirmation_becomes_confirmed(auth_client, user):
    challenge = make_challenge(needs_confirmation=False)
    joined = baker.make(
        'joined_challenge.JoinedChallenge',
        user=user, challenge=challenge, status=JoinedChallengeStatus.JOINED,
    )
    article = baker.make('joined_challenge.ArticleJoinedChallenge', main_joined_challenge=joined)
    payload = {'main_joined_challenge': {
        'challenge': str(challenge.uuid),
        'status': JoinedChallengeStatus.COMPLETED,
    }}

    response = auth_client(user).patch(f'{ARTICLE_JOINED_URL}{article.uuid}/', payload, format='json')

    assert response.status_code == 200
    joined.refresh_from_db()
    assert joined.status == JoinedChallengeStatus.CONFIRMED
