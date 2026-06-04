"""API tests for the challenge catalogue endpoints.

These are read-only and authenticated. The generic ``challenge`` endpoint only
lists *active* challenges (published and within their date window); the typed
endpoints only list challenges whose main challenge is published and current.
"""
import pytest
from model_bakery import baker

from challenge.models.base import ChallengeType

pytestmark = pytest.mark.django_db

CHALLENGE_URL = '/api/challenge/challenge/'
ARTICLE_CHALLENGE_URL = '/api/challenge/article_challenge/'


def make_full_challenge(make_challenge, published=True):
    """A Challenge plus its concrete ArticleChallenge (needed for serialization)."""
    challenge = make_challenge(type=ChallengeType.ARTICLE, published=published)
    baker.make('challenge.ArticleChallenge', main_challenge=challenge)
    return challenge


def test_challenges_require_authentication(api_client):
    response = api_client.get(CHALLENGE_URL)
    assert response.status_code in (401, 403)


def test_challenge_list_excludes_unpublished(auth_client, user, make_challenge):
    published = make_full_challenge(make_challenge, published=True)
    unpublished = make_full_challenge(make_challenge, published=False)

    response = auth_client(user).get(CHALLENGE_URL)

    assert response.status_code == 200
    uuids = [item['uuid'] for item in response.data]
    assert str(published.uuid) in uuids
    assert str(unpublished.uuid) not in uuids


def test_challenge_endpoint_is_read_only(auth_client, user):
    response = auth_client(user).post(CHALLENGE_URL, {'type': ChallengeType.ARTICLE, 'points': 1})
    assert response.status_code == 405


def test_article_challenge_excludes_invisible(auth_client, user, make_challenge):
    visible_main = make_challenge(type=ChallengeType.ARTICLE, published=True)
    visible = baker.make('challenge.ArticleChallenge', main_challenge=visible_main)
    hidden_main = make_challenge(type=ChallengeType.ARTICLE, published=False)
    hidden = baker.make('challenge.ArticleChallenge', main_challenge=hidden_main)

    response = auth_client(user).get(ARTICLE_CHALLENGE_URL)

    assert response.status_code == 200
    uuids = [item['uuid'] for item in response.data]
    assert str(visible.uuid) in uuids
    assert str(hidden.uuid) not in uuids
