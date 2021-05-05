import pytest

from challenge.models import ArticleChallenge, Challenge, JoinedChallenge
from challenge.models.challenge import ChallengeType
from challenge.models.joined_challenge import JoinedChallengeStatus, ArticleJoinedChallenge
from user.models import User


@pytest.fixture
def article_challenges():
    main_challenge1 = Challenge(
        type=ChallengeType.ARTICLE,
        name='test_challenge',
        points=5
    )

    main_challenge2 = Challenge(
        type=ChallengeType.ARTICLE,
        name='test_challenge',
        points=4
    )

    challenge1 = ArticleChallenge(
        main_challenge=main_challenge1
    )
    challenge2 = ArticleChallenge(
        main_challenge=main_challenge1
    )

    yield challenge1, challenge2

    challenge1.delete()
    challenge2.delete()
    main_challenge1.delete()
    main_challenge2.delete()


@pytest.fixture()
def users():
    user1 = User(email='email1@example.com', password="abc")
    user2 = User(email='email2@example.com', password="abc")
    yield user1, user2
    user1.delete()
    user2.delete()


@pytest.fixture
def joined_article_challenges(article_challenges, users):
    user1, user2 = users
    main_joined_challenge1_1 = JoinedChallenge(
        user=user1,
        challenge=article_challenges[0].main_challenge,
        status=JoinedChallengeStatus.JOINED,
    )
    main_joined_challenge1_2 = JoinedChallenge(
        user=user1,
        challenge=article_challenges[1].main_challenge,
        status=JoinedChallengeStatus.JOINED,
    )
    main_joined_challenge2_1 = JoinedChallenge(
        user=user2,
        challenge=article_challenges[0].main_challenge,
        status=JoinedChallengeStatus.JOINED,
    )
    article_joined_challenge1_1 = ArticleJoinedChallenge(
        main_joined_challenge=main_joined_challenge1_1,
        article_name='test article',
        article_url='example.com/article',
    )
    article_joined_challenge1_2 = ArticleJoinedChallenge(
        main_joined_challenge=main_joined_challenge1_2,
        article_name='test article',
        article_url='example.com/article',
    )
    article_joined_challenge2_1 = ArticleJoinedChallenge(
        main_joined_challenge=main_joined_challenge2_1,
        article_name='test article',
        article_url='example.com/article',
    )
    yield (article_joined_challenge1_1,
           article_joined_challenge1_2,
           article_joined_challenge2_1)

    article_joined_challenge1_1.delete()
    main_joined_challenge1_1.delete()


@pytest.fixture
def completed_article_challenges(joined_article_challenge):
    joined_article_challenge.main_joined_challenge.completed = True
    joined_article_challenge.main_joined_challenge.save()

