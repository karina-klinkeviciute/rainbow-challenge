import pytest
from model_bakery import baker

pytestmark = pytest.mark.django_db

@pytest.fixture
def user_1():
    return baker.make('user.User', email='testemail21@example.com')


@pytest.fixture
def user_2():
    return baker.make('user.User', email='testemail21@aha.com')


@pytest.fixture()
def quiz_user_1(user_1):
    return baker.make('quiz.QuizUser', user=user_1)


@pytest.fixture
def correct_answer(quiz_user_1):
    answer = baker.make('quiz.Answer', correct=True)
    user_answer = baker.make('quiz.UserAnswer', answer=answer, quiz_user=quiz_user_1)
    return user_answer

@pytest.fixture
def incorrect_answer(quiz_user_1):
    answer = baker.make('quiz.Answer', correct=False)
    user_answer = baker.make('quiz.UserAnswer', answer=answer, quiz_user=quiz_user_1)
    return user_answer
