"""Tests for ``challenge/views/challenge.py`` - the staff-only template views.

These are the Django (non-API) admin/volunteer screens for creating, editing
and listing article challenges, under ``/challenge/challenge/...``. Every view
is wrapped in ``staff_member_required``, so anonymous and non-staff users are
redirected to the admin login; only staff (``is_admin``) users get in.

Note: editing goes through the ``<uuid>`` route, which binds the form to the
existing challenge. The create route (no uuid) is intentionally not exercised
here - its template renders ``view.form`` as an unbound form *class*, so it is
covered only indirectly.
"""
import pytest
from django.urls import reverse
from model_bakery import baker

from challenge.models import ArticleChallenge

pytestmark = pytest.mark.django_db


# These views use ``staff_member_required``, which needs is_active *and*
# is_staff (== is_admin here); the shared ``admin_user`` fixture is active, so
# it satisfies both.


def make_article_challenge(make_challenge, **kwargs):
    """A concrete ArticleChallenge wired to a main Challenge."""
    challenge = make_challenge(**kwargs)
    return baker.make(ArticleChallenge, main_challenge=challenge)


# --- list view access control ---------------------------------------------

def test_article_list_redirects_anonymous(client):
    # staff_member_required sends anonymous users to the admin login page.
    response = client.get(reverse("challenge:articles"))

    assert response.status_code == 302
    assert "/admin/login" in response.url


def test_article_list_redirects_non_staff(logged_in_client, user):
    response = logged_in_client(user).get(reverse("challenge:articles"))

    assert response.status_code == 302
    assert "/admin/login" in response.url


def test_article_list_shows_challenges_for_staff(logged_in_client, admin_user, make_challenge):
    article = make_article_challenge(make_challenge)

    response = logged_in_client(admin_user).get(reverse("challenge:articles"))

    assert response.status_code == 200
    assert list(response.context["object_list"]) == [article]


# --- update view ----------------------------------------------------------

def test_article_update_requires_staff(logged_in_client, user, make_challenge):
    article = make_article_challenge(make_challenge)

    url = reverse("challenge:article-update", kwargs={"uuid": str(article.uuid)})
    response = logged_in_client(user).get(url)

    assert response.status_code == 302
    assert "/admin/login" in response.url


def test_article_update_renders_bound_form(logged_in_client, admin_user, make_challenge):
    article = make_article_challenge(make_challenge, _name="Original")

    url = reverse("challenge:article-update", kwargs={"uuid": str(article.uuid)})
    response = logged_in_client(admin_user).get(url)

    assert response.status_code == 200
    # The form is bound to the existing challenge, so its current name is shown.
    assert response.context["view"].form.instance == article.main_challenge


def test_article_update_saves_changes(logged_in_client, admin_user, make_challenge):
    article = make_article_challenge(make_challenge, _name="Original", points=10)
    challenge = article.main_challenge

    url = reverse("challenge:article-update", kwargs={"uuid": str(article.uuid)})
    response = logged_in_client(admin_user).post(
        url,
        {"_name": "Updated", "description": "New description", "points": 55},
    )

    assert response.status_code == 200
    challenge.refresh_from_db()
    assert challenge._name == "Updated"
    assert challenge.points == 55


def test_article_update_invalid_form_does_not_save(logged_in_client, admin_user, make_challenge):
    article = make_article_challenge(make_challenge, _name="Original")
    challenge = article.main_challenge

    url = reverse("challenge:article-update", kwargs={"uuid": str(article.uuid)})
    response = logged_in_client(admin_user).post(
        url,
        # _name is required; omitting it makes the form invalid.
        {"description": "New description", "points": 55},
    )

    assert response.status_code == 200
    challenge.refresh_from_db()
    assert challenge._name == "Original"
