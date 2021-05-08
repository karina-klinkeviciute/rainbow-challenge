from model_bakery.recipe import Recipe

from challenge.models import JoinedChallenge
from challenge.models.challenge import ChallengeType

joined_challenge_recipe = Recipe(
        JoinedChallenge,
        challenge__type=ChallengeType.ARTICLE
    )
