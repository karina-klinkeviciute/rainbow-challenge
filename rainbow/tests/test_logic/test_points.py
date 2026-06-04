"""Tests for point calculations on the User model and JoinedChallenge.

- quiz challenges are worth one point per correct answer;
- non-quiz challenges are worth their ``challenge.points`` once confirmed;
- only CONFIRMED challenges count;
- remaining points subtract the cost of claimed prizes.
"""
import pytest
from model_bakery import baker

from challenge.models.base import ChallengeType
from joined_challenge.models.base import JoinedChallengeStatus

pytestmark = pytest.mark.django_db


def confirmed_quiz(user, correct, incorrect):
    """A confirmed quiz challenge with the given number of correct/incorrect answers."""
    challenge = baker.make(
        'challenge.Challenge', type=ChallengeType.QUIZ, published=True,
        points=0, multiple=True, needs_confirmation=False,
    )
    joined = baker.make(
        'joined_challenge.JoinedChallenge', user=user, challenge=challenge,
        status=JoinedChallengeStatus.JOINED,
    )
    quiz_joined = baker.make('joined_challenge.QuizJoinedChallenge', main_joined_challenge=joined)
    baker.make('joined_challenge.UserAnswer', quiz_joined_challenge=quiz_joined, answer__correct=True, _quantity=correct)
    if incorrect:
        baker.make('joined_challenge.UserAnswer', quiz_joined_challenge=quiz_joined, answer__correct=False, _quantity=incorrect)
    # Flip to confirmed now that the concrete quiz challenge and answers exist.
    joined.status = JoinedChallengeStatus.CONFIRMED
    joined.save()
    return joined


def test_quiz_points_count_correct_answers_only(user, make_joined_challenge, make_challenge):
    confirmed_quiz(user, correct=2, incorrect=3)

    assert user.quiz_points == 2


def test_only_confirmed_challenges_count_towards_points(user, make_joined_challenge, make_challenge):
    confirmed = make_challenge(type=ChallengeType.ARTICLE, points=30)
    make_joined_challenge(user, challenge=confirmed, status=JoinedChallengeStatus.CONFIRMED)
    # A merely joined challenge must not contribute.
    joined_only = make_challenge(type=ChallengeType.ARTICLE, points=50)
    make_joined_challenge(user, challenge=joined_only, status=JoinedChallengeStatus.JOINED)

    assert user.all_points == 30


def test_all_points_combine_challenge_and_quiz_points(user, make_joined_challenge, make_challenge):
    article = make_challenge(type=ChallengeType.ARTICLE, points=30)
    make_joined_challenge(user, challenge=article, status=JoinedChallengeStatus.CONFIRMED)
    confirmed_quiz(user, correct=2, incorrect=1)

    assert user.all_points == 32


def test_remaining_points_subtract_claimed_prizes(user, make_joined_challenge, make_challenge):
    article = make_challenge(type=ChallengeType.ARTICLE, points=100)
    make_joined_challenge(user, challenge=article, status=JoinedChallengeStatus.CONFIRMED)
    prize = baker.make('results.Prize', price=10, amount=10)
    baker.make('results.ClaimedPrize', user=user, prize=prize, amount=3)

    assert user.all_points == 100
    assert user.remaining_points == 70


def test_final_points_for_non_quiz_is_challenge_points(user, make_joined_challenge, make_challenge):
    article = make_challenge(type=ChallengeType.ARTICLE, points=42)
    joined = make_joined_challenge(user, challenge=article, status=JoinedChallengeStatus.CONFIRMED)

    assert joined.final_points == 42


def test_final_points_for_quiz_is_correct_answer_count(user):
    joined = confirmed_quiz(user, correct=3, incorrect=2)

    assert joined.final_points == 3
