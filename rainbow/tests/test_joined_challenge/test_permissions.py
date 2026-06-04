"""Tests for joined challenge access permissions (issue #104).

Only the user themselves and admins may access a user's joined challenges.
"""
import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from joined_challenge.models import JoinedChallenge, ArticleJoinedChallenge
from joined_challenge.models.quiz import QuizJoinedChallenge, UserAnswer

pytestmark = pytest.mark.django_db

ARTICLE_URL = '/api/joined_challenge/article_joined_challenge/'
USER_ANSWER_URL = '/api/joined_challenge/user_answer/'


@pytest.fixture
def user():
    return baker.make('user.User', email='owner@example.com')


@pytest.fixture
def other_user():
    return baker.make('user.User', email='other@example.com')


@pytest.fixture
def admin_user():
    return baker.make('user.User', email='admin@example.com', is_admin=True)


def make_article(user):
    joined_challenge = baker.make(JoinedChallenge, user=user)
    return baker.make(ArticleJoinedChallenge, main_joined_challenge=joined_challenge)


def make_user_answer(user):
    quiz_joined_challenge = baker.make(QuizJoinedChallenge, main_joined_challenge__user=user)
    return baker.make(UserAnswer, quiz_joined_challenge=quiz_joined_challenge)


def authed_client(user):
    client = APIClient()
    client.force_authenticate(user)
    return client


def test_anonymous_cannot_list_joined_challenges():
    # secure=True so SECURE_SSL_REDIRECT does not 301 the request before the view.
    response = APIClient().get(ARTICLE_URL, secure=True)
    assert response.status_code in (401, 403)


def test_user_only_sees_own_joined_challenges(user, other_user):
    mine = make_article(user)
    make_article(other_user)

    response = authed_client(user).get(ARTICLE_URL, secure=True)

    assert response.status_code == 200
    assert [item['uuid'] for item in response.data] == [str(mine.uuid)]


def test_user_cannot_retrieve_another_users_joined_challenge(user, other_user):
    theirs = make_article(other_user)

    response = authed_client(user).get(f'{ARTICLE_URL}{theirs.uuid}/', secure=True)

    assert response.status_code == 404


def test_admin_does_not_see_others_joined_challenges_via_api(user, admin_user):
    # Admins get cross-user access only through the Django admin, not the API.
    mine = make_article(admin_user)
    make_article(user)

    response = authed_client(admin_user).get(ARTICLE_URL, secure=True)

    assert response.status_code == 200
    assert [item['uuid'] for item in response.data] == [str(mine.uuid)]


def test_user_only_sees_own_quiz_answers(user, other_user):
    mine = make_user_answer(user)
    make_user_answer(other_user)

    response = authed_client(user).get(USER_ANSWER_URL, secure=True)

    assert response.status_code == 200
    assert [item['uuid'] for item in response.data] == [str(mine.uuid)]


def test_admin_does_not_see_others_quiz_answers_via_api(user, admin_user):
    # Admins get cross-user access only through the Django admin, not the API.
    mine = make_user_answer(admin_user)
    make_user_answer(user)

    response = authed_client(admin_user).get(USER_ANSWER_URL, secure=True)

    assert response.status_code == 200
    assert [item['uuid'] for item in response.data] == [str(mine.uuid)]