"""Tests for derived values on the results models: region scores and prize stock."""
import pytest
from model_bakery import baker

from challenge.models.base import ChallengeType
from joined_challenge.models.base import JoinedChallengeStatus

pytestmark = pytest.mark.django_db


def test_region_points_sum_confirmed_challenges_of_its_users(
        make_user, make_joined_challenge, make_challenge):
    region = baker.make('results.Region', name='Kaunas')
    member_a = make_user(region=region)
    member_b = make_user(region=region)
    outsider = make_user()

    make_joined_challenge(member_a, challenge=make_challenge(points=20),
                          status=JoinedChallengeStatus.CONFIRMED)
    make_joined_challenge(member_b, challenge=make_challenge(points=30),
                          status=JoinedChallengeStatus.CONFIRMED)
    # Not confirmed -> ignored.
    make_joined_challenge(member_a, challenge=make_challenge(points=99),
                          status=JoinedChallengeStatus.JOINED)
    # Outside the region -> ignored.
    make_joined_challenge(outsider, challenge=make_challenge(points=100),
                          status=JoinedChallengeStatus.CONFIRMED)

    assert region.points == 50


def test_prize_amount_remaining_subtracts_claims(user, other_user):
    prize = baker.make('results.Prize', amount=10)
    baker.make('results.ClaimedPrize', prize=prize, user=user, amount=3)
    baker.make('results.ClaimedPrize', prize=prize, user=other_user, amount=2)

    assert prize.amount_remaining == 5


def test_prize_amount_remaining_with_no_claims_is_full_amount(db):
    prize = baker.make('results.Prize', amount=7)

    assert prize.amount_remaining == 7
