import pytest

from challenge.tests.factories import ArticleChallengeModelFactory

pytestmark = pytest.mark.django_db

@pytest.mark.django_db
def test_concrete_challenge_uuid():
    article_challenge = ArticleChallengeModelFactory()
    assert article_challenge.uuid == str(article_challenge.main_challenge.concrete_challenge_uuid)

def test_challenge_model():
    article_challenge = ArticleChallengeModelFactory()
    assert "ArticleChallenge" == article_challenge.main_challenge.challenge_model.__name__

