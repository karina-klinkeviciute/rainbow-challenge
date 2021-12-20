import pytest
from model_bakery import baker

from joined_challenge.models.base import JoinedChallengeStatus
from joined_challenge.models.quiz import QuizJoinedChallenge

pytestmark = pytest.mark.django_db


def test_quiz_points(user_1, quiz_user_1, correct_answer, incorrect_answer):
	"""
	User with 1 correct and 1 incorrect answer should have 1 quiz point.
	"""
	joined_challenge1 = baker.make_recipe(
	    'tests.quiz_confirmed_joined_challenge_recipe',
	    user=user_1,
	)
	quiz_joined_challenge1 = baker.make(
	    QuizJoinedChallenge,
	    main_joined_challenge=joined_challenge1,
	    quiz_user=quiz_user_1,
	)

	assert user_1.quiz_points == 1
