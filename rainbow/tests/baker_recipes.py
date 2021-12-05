from model_bakery.recipe import Recipe

from joined_challenge.models import JoinedChallenge
from challenge.models.base import ChallengeType

joined_challenge_recipe = Recipe(
        JoinedChallenge,
        challenge__type=ChallengeType.ARTICLE
    )
