"""API tests for the results endpoints: regions, prizes, claimed prizes, balance."""
import pytest
from model_bakery import baker

from challenge.models.base import ChallengeType
from joined_challenge.models.base import JoinedChallengeStatus

pytestmark = pytest.mark.django_db

REGION_URL = '/api/results/region/'
PRIZE_URL = '/api/results/prize/'
AVAILABLE_PRIZE_URL = '/api/results/available_prize/'
CLAIMED_PRIZE_URL = '/api/results/claimed_prize/'
BALANCE_URL = '/api/results/balance/'


def give_user_points(make_joined_challenge, make_challenge, user, points):
    """Confirm a non-quiz challenge worth ``points`` so the user can spend them."""
    challenge = make_challenge(type=ChallengeType.ARTICLE, points=points)
    return make_joined_challenge(user, challenge=challenge, status=JoinedChallengeStatus.CONFIRMED)


# --- regions (public read) ------------------------------------------------

def test_regions_are_readable_without_authentication(api_client):
    baker.make('results.Region', name='Vilnius')
    response = api_client.get(REGION_URL)
    assert response.status_code == 200
    assert 'Vilnius' in [item['name'] for item in response.data]


def test_regions_are_read_only(auth_client, user):
    response = auth_client(user).post(REGION_URL, {'name': 'X'})
    assert response.status_code == 405


# --- prizes ---------------------------------------------------------------

def test_prizes_require_authentication(api_client):
    response = api_client.get(PRIZE_URL)
    assert response.status_code in (401, 403)


def test_prizes_are_read_only(auth_client, user):
    response = auth_client(user).post(PRIZE_URL, {'name': 'X', 'price': 1, 'amount': 1})
    assert response.status_code == 405


def test_available_prize_excludes_unavailable(auth_client, user):
    available = baker.make('results.Prize', available=True, amount=5, name='available')
    baker.make('results.Prize', available=False, amount=5, name='unavailable')

    response = auth_client(user).get(AVAILABLE_PRIZE_URL)

    assert response.status_code == 200
    names = [item['name'] for item in response.data]
    assert 'available' in names
    assert 'unavailable' not in names


# --- claimed prizes -------------------------------------------------------

def test_claimed_prizes_require_authentication(api_client):
    response = api_client.get(CLAIMED_PRIZE_URL)
    assert response.status_code in (401, 403)


def test_user_only_sees_own_claimed_prizes(auth_client, user, other_user):
    prize = baker.make('results.Prize', price=1, amount=10)
    mine = baker.make('results.ClaimedPrize', user=user, prize=prize, amount=1)
    baker.make('results.ClaimedPrize', user=other_user, prize=prize, amount=1)

    response = auth_client(user).get(CLAIMED_PRIZE_URL)

    assert response.status_code == 200
    assert [item['uuid'] for item in response.data] == [str(mine.uuid)]


def test_claiming_prize_without_enough_points_is_rejected(auth_client, user):
    prize = baker.make('results.Prize', price=100, amount=10)

    response = auth_client(user).post(CLAIMED_PRIZE_URL, {'prize': str(prize.uuid), 'amount': 1})

    assert response.status_code == 400


def test_claiming_prize_with_enough_points_succeeds(
        auth_client, user, make_joined_challenge, make_challenge):
    give_user_points(make_joined_challenge, make_challenge, user, points=100)
    prize = baker.make('results.Prize', price=10, amount=10)

    response = auth_client(user).post(CLAIMED_PRIZE_URL, {'prize': str(prize.uuid), 'amount': 2})

    assert response.status_code == 201
    assert user.claimedprize_set.count() == 1


# --- balance --------------------------------------------------------------

def test_balance_requires_authentication(api_client):
    response = api_client.get(BALANCE_URL)
    assert response.status_code in (401, 403)


def test_balance_reports_earned_and_remaining(
        auth_client, user, make_joined_challenge, make_challenge):
    give_user_points(make_joined_challenge, make_challenge, user, points=70)

    response = auth_client(user).get(BALANCE_URL)

    assert response.status_code == 200
    assert response.data['earned_rainbows'] == 70
    assert response.data['remaining_rainbows'] == 70
    assert len(response.data['earning']) == 1
