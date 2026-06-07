"""API tests for the user-facing endpoints under /api/user/.

Covers the public gender list and the authenticated "my joined / completed
challenges" listings (which are scoped to the requesting user and filtered by
status).
"""
import pytest
from model_bakery import baker

from challenge.models.base import ChallengeType
from joined_challenge.models.base import JoinedChallengeStatus

pytestmark = pytest.mark.django_db

GENDER_URL = '/api/user/gender/'
JOINED_URL = '/api/user/joined_challenges'
COMPLETED_URL = '/api/user/completed_challenges'


def full_joined_challenge(user, status):
    """A fully wired joined challenge so JoinedChallengeSerializer can render it."""
    challenge = baker.make('challenge.Challenge', type=ChallengeType.ARTICLE, published=True, points=10)
    baker.make('challenge.ArticleChallenge', main_challenge=challenge)
    joined = baker.make('joined_challenge.JoinedChallenge', user=user, challenge=challenge, status=status)
    baker.make('joined_challenge.ArticleJoinedChallenge', main_joined_challenge=joined)
    return joined


# --- gender (public) ------------------------------------------------------

def test_gender_list_is_public(api_client):
    response = api_client.get(GENDER_URL)
    assert response.status_code == 200
    assert response.data


# --- my joined challenges -------------------------------------------------

def test_joined_challenges_require_authentication(api_client):
    response = api_client.get(JOINED_URL)
    assert response.status_code in (401, 403)


def test_joined_challenges_lists_only_own_joined(auth_client, user, other_user):
    mine = full_joined_challenge(user, JoinedChallengeStatus.JOINED)
    full_joined_challenge(user, JoinedChallengeStatus.CONFIRMED)  # wrong status, excluded
    full_joined_challenge(other_user, JoinedChallengeStatus.JOINED)  # other user, excluded

    response = auth_client(user).get(JOINED_URL)

    assert response.status_code == 200
    assert [item['uuid'] for item in response.data] == [str(mine.uuid)]


# --- my completed challenges ----------------------------------------------

def test_completed_challenges_require_authentication(api_client):
    response = api_client.get(COMPLETED_URL)
    assert response.status_code in (401, 403)


def test_completed_challenges_lists_confirmed_and_completed(auth_client, user):
    confirmed = full_joined_challenge(user, JoinedChallengeStatus.CONFIRMED)
    completed = full_joined_challenge(user, JoinedChallengeStatus.COMPLETED)
    full_joined_challenge(user, JoinedChallengeStatus.JOINED)  # excluded

    response = auth_client(user).get(COMPLETED_URL)

    assert response.status_code == 200
    uuids = {item['uuid'] for item in response.data}
    assert uuids == {str(confirmed.uuid), str(completed.uuid)}
