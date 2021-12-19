from model_bakery.recipe import Recipe

from joined_challenge.models import JoinedChallenge
from joined_challenge.models.base import JoinedChallengeStatus
from challenge.models.base import ChallengeType

joined_challenge_recipe = Recipe(
        JoinedChallenge,
        challenge__type=ChallengeType.ARTICLE,
        status=JoinedChallengeStatus.JOINED,
    )

confirmed_joined_challenge_recipe = Recipe(
        JoinedChallenge,
        challenge__type=ChallengeType.ARTICLE,
        status=JoinedChallengeStatus.CONFIRMED
    )

quiz_confirmed_joined_challenge_recipe = Recipe(
        JoinedChallenge,
        challenge__type=ChallengeType.QUIZ,
        status=JoinedChallengeStatus.CONFIRMED
    )