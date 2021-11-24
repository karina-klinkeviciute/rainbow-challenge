import pytest
from model_bakery import baker
from faker import Faker

from joined_challenge.models.base import JoinedChallengeStatus

faker = Faker()


def test_all_points():
    """
    Tests if calculation of all points is alright:

    Create user
    Create challenges with points
    Create joined challenges for those challenges and user
    complete those challenges
    count their points and check if it's calculated alright
    """

    user1 = baker.make('user.User', email='testemail21@example.com')
    user2 = baker.make('user.User', email='testemail21@aha.com')

    joined_challenge1 = baker.make_recipe(
        'user.joined_challenge_recipe',
        user=user1,
        status=JoinedChallengeStatus.COMPLETED,
    )

    joined_challenge2 = baker.make_recipe(
        'user.joined_challenge_recipe',
        user=user1,
        status=JoinedChallengeStatus.COMPLETED,
    )

    joined_challenge3 = baker.make_recipe(
        'user.joined_challenge_recipe',
        user=user2,
        status=JoinedChallengeStatus.COMPLETED,
    )

    joined_challenge4 = baker.make_recipe(
        'user.joined_challenge_recipe',
        user=user1,
        status=JoinedChallengeStatus.JOINED)

    assert user1.all_points == joined_challenge1.challenge.points + joined_challenge2.challenge.points

    user1.delete()
    user2.delete()
    joined_challenge1.delete()
    joined_challenge2.delete()
    joined_challenge3.delete()
    joined_challenge4.delete()
