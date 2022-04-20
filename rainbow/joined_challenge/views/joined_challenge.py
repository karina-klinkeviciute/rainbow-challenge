from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from challenge.models.quiz import Answer
from joined_challenge.models import JoinedChallenge, ArticleJoinedChallenge, EventParticipantJoinedChallenge, \
    SchoolGSAJoinedChallenge, EventOrganizerJoinedChallenge, StoryJoinedChallenge, ProjectJoinedChallenge, \
    ReactingJoinedChallenge, SupportJoinedChallenge, CustomJoinedChallenge, QuizJoinedChallenge
from joined_challenge.models.base import JoinedChallengeStatus
from joined_challenge.models.quiz import UserAnswer
from joined_challenge.serializers.joined_challenge import (
    JoinedChallengeSerializer,
    ArticleJoinedChallengeSerializer,
    EventParticipantJoinedChallengeSerializer, SchoolGSAJoinedChallengeSerializer,
    EventOrganizerJoinedChallengeSerializer, StoryJoinedChallengeSerializer, ProjectJoinedChallengeSerializer,
    ReactingJoinedChallengeSerializer, SupportJoinedChallengeSerializer, CustomJoinedChallengeSerializer,
    QuizJoinedChallengeSerializer, UserAnswerSerializer)


class JoinedChallengeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing JoinedChallenge instances.
    """
    serializer_class = JoinedChallengeSerializer
    queryset = JoinedChallenge.objects.all()


class BaseJoinedChallengeViewset(viewsets.ModelViewSet):
    """Base viewset for joined challenges of dihherent typse"""
    http_method_names = ('get', 'head', 'options', 'post', 'patch', 'delete')


class ArticleJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Article.
    """
    serializer_class = ArticleJoinedChallengeSerializer
    queryset = ArticleJoinedChallenge.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(main_joined_challenge__user=self.request.user)


class EventParticipantJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Event Participant.
    """
    serializer_class = EventParticipantJoinedChallengeSerializer
    queryset = EventParticipantJoinedChallenge.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(main_joined_challenge__user=self.request.user)


class SchoolGSAJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type School GSA.
    """
    serializer_class = SchoolGSAJoinedChallengeSerializer
    queryset = SchoolGSAJoinedChallenge.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(main_joined_challenge__user=self.request.user)


class EventOrganizerJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Event Organizer.
    """
    serializer_class = EventOrganizerJoinedChallengeSerializer
    queryset = EventOrganizerJoinedChallenge.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(main_joined_challenge__user=self.request.user)


class StoryJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Story.
    """
    serializer_class = StoryJoinedChallengeSerializer
    queryset = StoryJoinedChallenge.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(main_joined_challenge__user=self.request.user)


class ProjectJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Project.
    """
    serializer_class = ProjectJoinedChallengeSerializer
    queryset = ProjectJoinedChallenge.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(main_joined_challenge__user=self.request.user)


class ReactingJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Reacting.
    """
    serializer_class = ReactingJoinedChallengeSerializer
    queryset = ReactingJoinedChallenge.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(main_joined_challenge__user=self.request.user)


class SupportJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Support.
    """
    serializer_class = SupportJoinedChallengeSerializer
    queryset = SupportJoinedChallenge.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(main_joined_challenge__user=self.request.user)


class CustomJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Custom.
    """
    serializer_class = CustomJoinedChallengeSerializer
    queryset = CustomJoinedChallenge.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(main_joined_challenge__user=self.request.user)


class QuizJoinedChallengeViewSet(BaseJoinedChallengeViewset):
    """
    Challenges of type Quiz.
    """
    serializer_class = QuizJoinedChallengeSerializer
    queryset = QuizJoinedChallenge.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(main_joined_challenge__user=self.request.user)


class UserAnswerViewSet(viewsets.ModelViewSet):
    serializer_class = UserAnswerSerializer
    queryset = UserAnswer.objects.all()


class UserJoinedChallengesAPIView(ListAPIView):
    serializer_class = JoinedChallengeSerializer

    def get_queryset(self):
        queryset = JoinedChallenge.objects.all()
        user = self.request.user
        if user is not None:
            queryset = queryset.filter(
                user=user,
                status=JoinedChallengeStatus.JOINED
            )
        return queryset


class UserCompletedChallengesAPIView(ListAPIView):
    serializer_class = JoinedChallengeSerializer

    def get_queryset(self):
        queryset = JoinedChallenge.objects.all()
        user = self.request.user
        if user is not None:
            queryset = queryset.filter(
                user=user,
                status__in=(JoinedChallengeStatus.CONFIRMED, JoinedChallengeStatus.COMPLETED)
            )
        return queryset
