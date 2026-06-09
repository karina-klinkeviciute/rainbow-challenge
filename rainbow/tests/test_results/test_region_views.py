"""Tests for ``results/views/region.py``.

``RegionViewSet`` powers the public ``/api/results/region/`` leaderboard, listing
regions ordered by their (computed) points, highest first.

``RegionUsersAPIView`` and ``RegionChallengesAPIView`` filter users / active
challenges by region. They are imported in ``challenge/urls.py`` but not wired to
any URL, so they're exercised here at the ``get_queryset`` level directly rather
than over HTTP.
"""
import pytest
from model_bakery import baker

from challenge.models import Challenge
from joined_challenge.models.base import JoinedChallengeStatus
from results.models.region import Region
from results.views.region import RegionChallengesAPIView, RegionUsersAPIView

pytestmark = pytest.mark.django_db

REGION_URL = "/api/results/region/"


# --- RegionViewSet (public leaderboard) -----------------------------------

def test_region_list_is_public(api_client):
    baker.make(Region, name="Solo")
    response = api_client.get(REGION_URL)

    assert response.status_code == 200
    assert {r["name"] for r in response.data} == {"Solo"}


def test_region_list_is_ordered_by_points_desc(
    api_client, make_user, make_challenge, make_joined_challenge,
):
    high = baker.make(Region, name="High")
    low = baker.make(Region, name="Low")  # no members -> 0 points

    # Give "High" a member with a CONFIRMED challenge worth 50 points.
    member = make_user(region=high)
    challenge = make_challenge(points=50, region=high)
    make_joined_challenge(
        member, challenge=challenge, status=JoinedChallengeStatus.CONFIRMED,
    )

    response = api_client.get(REGION_URL)

    assert response.status_code == 200
    names = [r["name"] for r in response.data]
    assert names == ["High", "Low"]


# --- RegionUsersAPIView (unrouted; queryset tested directly) ---------------

def test_region_users_filters_by_region(make_user):
    region = baker.make(Region, name="R")
    in_region = make_user(region=region)
    make_user()  # no region

    view = RegionUsersAPIView()
    view.kwargs = {"region_uuid": region.uuid}

    assert list(view.get_queryset()) == [in_region]


def test_region_users_without_region_returns_all(make_user):
    make_user()
    make_user()

    view = RegionUsersAPIView()
    view.kwargs = {}

    assert view.get_queryset().count() == 2


# --- RegionChallengesAPIView (unrouted; queryset tested directly) ----------

def test_region_challenges_filters_by_region(make_challenge):
    region = baker.make(Region, name="R")
    in_region = make_challenge(region=region)
    make_challenge()  # no region

    view = RegionChallengesAPIView()
    view.kwargs = {"region_uuid": region.uuid}

    assert list(view.get_queryset()) == [in_region]


def test_region_challenges_without_region_returns_all_active(make_challenge):
    make_challenge()
    make_challenge()

    view = RegionChallengesAPIView()
    view.kwargs = {}

    assert view.get_queryset().count() == Challenge.active.count()
