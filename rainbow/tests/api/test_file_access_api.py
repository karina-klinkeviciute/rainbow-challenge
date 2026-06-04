"""API tests for joined-challenge file listing access control (issue #104).

Through the API only the owning user may list a joined challenge's files;
other users (including admins) are refused. Cross-user access is reserved for
the Django admin interface.
"""
import pytest
from model_bakery import baker

from challenge.models.base import ChallengeType
from joined_challenge.models.base import JoinedChallengeStatus

pytestmark = pytest.mark.django_db

CONCRETE_FILE_LIST = '/api/concrete_joined_challenge_file_list/article/{uuid}/'
JOINED_FILE_LIST = '/api/joined_challenge_file_list/{uuid}/'


def make_article_joined(user):
    challenge = baker.make(
        'challenge.Challenge', type=ChallengeType.ARTICLE, published=True,
        points=10, multiple=True, needs_confirmation=False,
    )
    joined = baker.make(
        'joined_challenge.JoinedChallenge', user=user, challenge=challenge,
        status=JoinedChallengeStatus.JOINED,
    )
    article = baker.make('joined_challenge.ArticleJoinedChallenge', main_joined_challenge=joined)
    return joined, article


# --- concrete joined challenge file list ----------------------------------

def test_concrete_file_list_requires_authentication(api_client, user):
    _, article = make_article_joined(user)
    response = api_client.get(CONCRETE_FILE_LIST.format(uuid=article.uuid))
    assert response.status_code in (401, 403)


def test_concrete_file_list_visible_to_owner(auth_client, user):
    _, article = make_article_joined(user)
    response = auth_client(user).get(CONCRETE_FILE_LIST.format(uuid=article.uuid))
    assert response.status_code == 200


def test_concrete_file_list_forbidden_to_other_user(auth_client, user, other_user):
    _, article = make_article_joined(user)
    response = auth_client(other_user).get(CONCRETE_FILE_LIST.format(uuid=article.uuid))
    assert response.status_code == 403


def test_concrete_file_list_forbidden_to_admin_via_api(auth_client, user, admin_user):
    _, article = make_article_joined(user)
    response = auth_client(admin_user).get(CONCRETE_FILE_LIST.format(uuid=article.uuid))
    assert response.status_code == 403


# --- main joined challenge file list --------------------------------------

def test_joined_file_list_visible_to_owner(auth_client, user):
    joined, _ = make_article_joined(user)
    response = auth_client(user).get(JOINED_FILE_LIST.format(uuid=joined.uuid))
    assert response.status_code == 200


def test_joined_file_list_hidden_from_other_user(auth_client, user, other_user):
    joined, _ = make_article_joined(user)
    response = auth_client(other_user).get(JOINED_FILE_LIST.format(uuid=joined.uuid))
    assert response.status_code == 404
