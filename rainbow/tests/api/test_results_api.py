"""API tests for the results endpoints: regions, prizes, claimed prizes, balance."""
import pytest
from model_bakery import baker
from rest_framework.test import APIRequestFactory

from challenge.models.base import ChallengeType
from joined_challenge.models.base import JoinedChallengeStatus
from results.permissions import IsClaimedPrizeOwner

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


def test_user_cannot_retrieve_another_users_claimed_prize(auth_client, user, other_user):
    prize = baker.make('results.Prize', price=1, amount=10)
    theirs = baker.make('results.ClaimedPrize', user=other_user, prize=prize, amount=1)

    response = auth_client(user).get(f'{CLAIMED_PRIZE_URL}{theirs.uuid}/')

    assert response.status_code == 404


def test_admin_does_not_see_others_claimed_prizes_via_api(auth_client, user, admin_user):
    # Admins get cross-user access only through the Django admin, not the API.
    prize = baker.make('results.Prize', price=1, amount=10)
    mine = baker.make('results.ClaimedPrize', user=admin_user, prize=prize, amount=1)
    baker.make('results.ClaimedPrize', user=user, prize=prize, amount=1)

    response = auth_client(admin_user).get(CLAIMED_PRIZE_URL)

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


def test_claiming_more_than_available_stock_is_rejected(
        auth_client, user, make_joined_challenge, make_challenge):
    # Enough points, but not enough stock -> the stock check must reject it.
    give_user_points(make_joined_challenge, make_challenge, user, points=100)
    prize = baker.make('results.Prize', price=1, amount=2)

    response = auth_client(user).post(CLAIMED_PRIZE_URL, {'prize': str(prize.uuid), 'amount': 3})

    assert response.status_code == 400
    assert user.claimedprize_set.count() == 0


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


# --- IsClaimedPrizeOwner (object-level ownership guard) --------------------

def _object_request(as_user):
    request = APIRequestFactory().get("/")
    request.user = as_user
    return request


def test_claimed_prize_owner_permission_allows_only_the_owner(user, other_user):
    prize = baker.make('results.Prize', price=1, amount=10)
    claimed = baker.make('results.ClaimedPrize', user=user, prize=prize, amount=1)
    permission = IsClaimedPrizeOwner()

    assert permission.has_object_permission(_object_request(user), None, claimed) is True
    assert permission.has_object_permission(_object_request(other_user), None, claimed) is False


def test_claimed_prize_owner_permission_excludes_admins(user, admin_user):
    # Cross-user access is reserved for the Django admin interface, so even an
    # admin is denied object access through this API permission.
    prize = baker.make('results.Prize', price=1, amount=10)
    claimed = baker.make('results.ClaimedPrize', user=user, prize=prize, amount=1)
    permission = IsClaimedPrizeOwner()

    assert permission.has_object_permission(_object_request(admin_user), None, claimed) is False
