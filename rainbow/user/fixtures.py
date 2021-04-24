import pytest

from challenge.models import ArticleChallenge, Challenge
from challenge.models.challenge import ChallengeType


@pytest.fixture
def completed_challenges():

    main_challenge = Challenge(
        type=ChallengeType.ARTICLE,
        name='test_challenge',
    )

    article_challenge = ArticleChallenge(
        main_challenge=main_challenge
    )
