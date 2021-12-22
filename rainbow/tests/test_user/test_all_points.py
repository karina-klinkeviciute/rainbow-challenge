import pytest
from model_bakery import baker

from joined_challenge.models.base import JoinedChallengeStatus

pytestmark = pytest.mark.django_db


def test_all_points(user_1, user_2):
    """
    Tests if calculation of all points is alright:

    Create user
    Create challenges with points
    Create joined challenges for those challenges and user
    complete those challenges
    count their points and check if it's calculated alright
    """
    joined_challenge1 = baker.make_recipe(
        'tests.confirmed_joined_challenge_recipe',
        user=user_1,
    )

    joined_challenge2 = baker.make_recipe(
        'tests.confirmed_joined_challenge_recipe',
        user=user_1,
    )

    joined_challenge3 = baker.make_recipe(
        'tests.confirmed_joined_challenge_recipe',
        user=user_2,
    )

    joined_challenge4 = baker.make_recipe(
        'tests.joined_challenge_recipe',
        user=user_1,)

    assert user_1.all_points == joined_challenge1.challenge.points + joined_challenge2.challenge.points
