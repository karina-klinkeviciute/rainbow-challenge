"""Shared pytest fixtures for the whole test suite.

Lives at the project root so every test module (top-level ``tests/`` and the
per-app test packages) can use these fixtures without importing anything.
"""
import pytest
from django.test import Client
from model_bakery import baker
from rest_framework.test import APIClient

from challenge.models.base import ChallengeType
from joined_challenge.models.base import JoinedChallengeStatus


# --- Users ----------------------------------------------------------------

@pytest.fixture
def make_user(db):
    """Factory creating distinct users; pass overrides as keyword arguments."""
    counter = {"n": 0}

    def _make_user(**kwargs):
        counter["n"] += 1
        kwargs.setdefault("email", f"user{counter['n']}@example.com")
        return baker.make("user.User", **kwargs)

    return _make_user


@pytest.fixture
def user(make_user):
    return make_user()


@pytest.fixture
def other_user(make_user):
    return make_user()


@pytest.fixture
def admin_user(make_user):
    # Active, like any real admin who can log in: some staff-only views go
    # through staff_member_required, which requires is_active as well as is_staff.
    return make_user(is_admin=True, is_active=True)


# --- API clients ----------------------------------------------------------

@pytest.fixture
def api_client():
    """An unauthenticated DRF test client."""
    return APIClient()


@pytest.fixture
def auth_client():
    """Factory returning an APIClient authenticated as the given user."""
    def _auth_client(user):
        client = APIClient()
        client.force_authenticate(user)
        return client

    return _auth_client


@pytest.fixture
def logged_in_client():
    """Factory returning a Django test ``Client`` logged in as the given user.

    The template-view (non-DRF) counterpart of ``auth_client``; use it for the
    dashboard / confirmation / challenge admin screens.
    """
    def _logged_in_client(user):
        client = Client()
        client.force_login(user)
        return client

    return _logged_in_client


# --- Domain object factories ---------------------------------------------

@pytest.fixture
def make_challenge(db):
    """Factory for ``Challenge`` rows, published and active by default."""
    def _make_challenge(**kwargs):
        kwargs.setdefault("type", ChallengeType.ARTICLE)
        kwargs.setdefault("points", 10)
        kwargs.setdefault("published", True)
        return baker.make("challenge.Challenge", **kwargs)

    return _make_challenge


@pytest.fixture
def make_joined_challenge(make_challenge):
    """Factory for ``JoinedChallenge`` rows tied to a user."""
    def _make_joined_challenge(user, challenge=None, status=JoinedChallengeStatus.JOINED, **kwargs):
        if challenge is None:
            challenge = make_challenge(type=kwargs.pop("type", ChallengeType.ARTICLE))
        return baker.make(
            "joined_challenge.JoinedChallenge",
            user=user,
            challenge=challenge,
            status=status,
            **kwargs,
        )

    return _make_joined_challenge
