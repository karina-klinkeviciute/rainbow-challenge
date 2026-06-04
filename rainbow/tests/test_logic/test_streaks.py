"""Tests for the weekly streak counter and medal issuing (User.update_streak).

Streaks increase by one per *week* a user is active; once a week is counted it
is not counted again. Reaching streak levels 10/20/30/40 issues a
bronze/silver/gold/platinum medal (once each) and an in-app message.
"""
import pytest
from model_bakery import baker

from message.models import Message, MessageTypes
from results.models.medal import Medal, MedalTypes
from results.models.streak import Streak

pytestmark = pytest.mark.django_db


def prior_streak(user, streaks):
    """A streak row from a past week, so update_streak() treats it as previous."""
    return baker.make('results.Streak', user=user, streaks=streaks, week=1, year=2000, change=1)


def test_first_streak_starts_at_one(user):
    user.update_streak()

    streak = Streak.objects.get(user=user)
    assert streak.streaks == 1


def test_streak_is_not_counted_twice_in_the_same_week(user):
    user.update_streak()
    user.update_streak()

    assert Streak.objects.filter(user=user).count() == 1


def test_streak_increments_in_a_new_week(user):
    prior_streak(user, streaks=1)

    user.update_streak()

    assert Streak.objects.filter(user=user).count() == 2
    assert Streak.objects.filter(user=user, streaks=2).exists()


def test_reaching_streak_ten_issues_a_bronze_medal_and_message(user):
    prior_streak(user, streaks=9)

    user.update_streak()  # -> 10

    assert Medal.objects.filter(user=user, level=MedalTypes.BRONZE).exists()
    assert Message.objects.filter(user=user, type=MessageTypes.MEDAL).exists()


def test_streak_below_threshold_issues_no_medal(user):
    prior_streak(user, streaks=4)

    user.update_streak()  # -> 5, not a medal level

    assert not Medal.objects.filter(user=user).exists()


def test_streak_property_reports_latest(user):
    prior_streak(user, streaks=1)
    user.update_streak()  # -> 2

    assert user.streak == {"streak": 2, "change": 1}
