from rest_framework import viewsets

from quiz.models import Quiz, QuizUser, Question, Answer, UserAnswer
from quiz.serializers import (
    QuizSerializer,
    QuizUserSerializer,
    QuestionSerializer,
    AnswerSerializer,
    UserAnswerSerializer
)


class QuizViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for EventOrganizer challenges.
    """
    http_method_names = ('get', 'head', 'options')
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()


class QuizUserViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for EventOrganizer challenges.
    """
    serializer_class = QuizUserSerializer
    queryset = QuizUser.objects.all()


class QuestionViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for EventOrganizer challenges.
    """
    http_method_names = ('get', 'head', 'options')
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


class AnswerViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for EventOrganizer challenges.
    """
    http_method_names = ('get', 'head', 'options')
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()


class UserAnswerViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for EventOrganizer challenges.
    """
    serializer_class = UserAnswerSerializer
    queryset = UserAnswer.objects.all()

