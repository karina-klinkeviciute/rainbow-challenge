"""Tests for the challenge-confirmation dashboard views.

These are the Django template views under ``/dashboard/confirmation/`` (not the
DRF API). Confirming a challenge awards points, so it is restricted to staff
(admin) users. A staff member opens the list of challenges a user marked
COMPLETED and confirms them; confirming flips the ``JoinedChallenge`` status to
CONFIRMED, which - through the model's ``save()`` - notifies the owner with an
in-app message.
"""
import pytest
from django.test import Client
from django.urls import reverse

from joined_challenge.models.base import JoinedChallengeStatus
from message.models import Message, MessageTypes

pytestmark = pytest.mark.django_db


# --- access control -------------------------------------------------------

def test_confirmation_list_requires_login():
    # LoginRequiredMixin redirects anonymous users to the login page.
    response = Client().get(reverse("confirmation-list"))

    assert response.status_code == 302


def test_confirmation_list_forbidden_for_non_staff(logged_in_client, user):
    # A logged-in, non-admin user is rejected (not redirected).
    response = logged_in_client(user).get(reverse("confirmation-list"))

    assert response.status_code == 403


def test_non_staff_cannot_confirm(logged_in_client, user, make_challenge, make_joined_challenge):
    challenge = make_challenge(needs_confirmation=False)
    joined = make_joined_challenge(
        user, challenge=challenge, status=JoinedChallengeStatus.COMPLETED,
    )

    url = reverse("confirmation-detail", kwargs={"pk": joined.uuid})
    response = logged_in_client(user).post(url)

    assert response.status_code == 403
    joined.refresh_from_db()
    assert joined.status == JoinedChallengeStatus.COMPLETED


# --- staff happy paths ----------------------------------------------------

def test_confirmation_list_shows_only_completed(logged_in_client, admin_user, user, make_joined_challenge):
    completed = make_joined_challenge(user, status=JoinedChallengeStatus.COMPLETED)
    make_joined_challenge(user, status=JoinedChallengeStatus.JOINED)
    make_joined_challenge(user, status=JoinedChallengeStatus.CONFIRMED)

    response = logged_in_client(admin_user).get(reverse("confirmation-list"))

    assert response.status_code == 200
    assert list(response.context["object_list"]) == [completed]


def test_staff_can_confirm_challenge_and_redirects(
    logged_in_client, admin_user, user, make_challenge, make_joined_challenge,
):
    challenge = make_challenge(needs_confirmation=False)
    joined = make_joined_challenge(
        user, challenge=challenge, status=JoinedChallengeStatus.COMPLETED,
    )

    url = reverse("confirmation-detail", kwargs={"pk": joined.uuid})
    response = logged_in_client(admin_user).post(url)

    assert response.status_code == 302
    assert response.url == reverse("confirmation-list")

    joined.refresh_from_db()
    assert joined.status == JoinedChallengeStatus.CONFIRMED


def test_confirming_notifies_the_owner(
    logged_in_client, admin_user, user, make_challenge, make_joined_challenge,
):
    challenge = make_challenge(needs_confirmation=False)
    joined = make_joined_challenge(
        user, challenge=challenge, status=JoinedChallengeStatus.COMPLETED,
    )

    url = reverse("confirmation-detail", kwargs={"pk": joined.uuid})
    logged_in_client(admin_user).post(url)

    # The message goes to the challenge owner, not to the confirming staff user.
    message = Message.objects.get(user=user, type=MessageTypes.CHALLENGE_CONFIRMATION)
    assert str(challenge.points) in message.message_text


def test_confirmation_detail_renders(logged_in_client, admin_user, user, make_joined_challenge):
    joined = make_joined_challenge(user, status=JoinedChallengeStatus.COMPLETED)

    response = logged_in_client(admin_user).get(
        reverse("confirmation-detail", kwargs={"pk": joined.uuid}),
    )

    assert response.status_code == 200


def test_confirmation_list_is_ordered_oldest_first(
    logged_in_client, admin_user, user, make_joined_challenge,
):
    # The queue is worked through FIFO: oldest completed submission first.
    import datetime

    older = make_joined_challenge(
        user, status=JoinedChallengeStatus.COMPLETED,
        completed_at=datetime.datetime(2024, 1, 1, tzinfo=datetime.timezone.utc),
    )
    newer = make_joined_challenge(
        user, status=JoinedChallengeStatus.COMPLETED,
        completed_at=datetime.datetime(2024, 6, 1, tzinfo=datetime.timezone.utc),
    )

    response = logged_in_client(admin_user).get(reverse("confirmation-list"))

    assert list(response.context["object_list"]) == [older, newer]