"""Tests for the dashboard landing view.

The dashboard links to admin-only actions (confirmation, etc.), so it is
staff-gated via the shared StaffRequiredMixin: anonymous users are redirected to
login, authenticated non-admins get a 403, and staff see the page.
"""
import pytest
from django.test import Client
from django.urls import reverse

from model_bakery import baker

from joined_challenge.models.base import JoinedChallengeStatus

pytestmark = pytest.mark.django_db


def test_dashboard_requires_login():
    response = Client().get(reverse("dashboard"))

    assert response.status_code == 302


def test_dashboard_forbidden_for_non_staff(logged_in_client, user):
    response = logged_in_client(user).get(reverse("dashboard"))

    assert response.status_code == 403


def test_dashboard_renders_for_staff(logged_in_client, admin_user):
    response = logged_in_client(admin_user).get(reverse("dashboard"))

    assert response.status_code == 200


def test_dashboard_shows_pending_confirmation_count(
    logged_in_client, admin_user, user, make_joined_challenge,
):
    # Two submissions waiting (COMPLETED); others should not be counted.
    make_joined_challenge(user, status=JoinedChallengeStatus.COMPLETED)
    make_joined_challenge(user, status=JoinedChallengeStatus.COMPLETED)
    make_joined_challenge(user, status=JoinedChallengeStatus.JOINED)
    make_joined_challenge(user, status=JoinedChallengeStatus.CONFIRMED)

    response = logged_in_client(admin_user).get(reverse("dashboard"))

    assert response.status_code == 200
    assert response.context["pending_confirmations_count"] == 2


def test_dashboard_shows_pending_prize_issuance_count(logged_in_client, admin_user, user):
    # Two claimed prizes waiting (issued=False); an already-issued one is excluded.
    baker.make("results.ClaimedPrize", user=user, issued=False, amount=1)
    baker.make("results.ClaimedPrize", user=user, issued=False, amount=1)
    baker.make("results.ClaimedPrize", user=user, issued=True, amount=1)

    response = logged_in_client(admin_user).get(reverse("dashboard"))

    assert response.status_code == 200
    assert response.context["pending_prize_issuance_count"] == 2
