import datetime

from django.db.models import Q
from rest_framework import viewsets, mixins

from challenge.models import SupportChallenge, ArticleChallenge, EventParticipantChallenge, CustomChallenge
from challenge.models.base import Challenge
from challenge.models.event_organizer import EventOrganizerChallenge
from challenge.models.project import ProjectChallenge
from challenge.models.reacting import ReactingChallenge
from challenge.models.school_gsa import SchoolGSAChallenge
from challenge.models.story import StoryChallenge
from challenge.serializers.challenge import ChallengeSerializer, ArticleChallengeSerializer, \
    EventParticipantChallengeSerializer, SchoolGSAChallengeSerializer, EventOrganizerChallengeSerializer, \
    StoryChallengeSerializer, ProjectChallengeSerializer, ReactingChallengeSerializer, SupportChallengeSerializer, \
    QuizChallengeSerializer, CustomChallengeSerializer


class ChallengeViewSet(
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """
    A viewset for viewing Challenge instances.
    """
    http_method_names = ('get', )
    serializer_class = ChallengeSerializer
    queryset = Challenge.active.all()


query_challenge_visible = Q(
    Q(main_challenge__published=True),
    Q(main_challenge__start_date__lte=datetime.datetime.now()) | Q(main_challenge__start_date__isnull=True),
    Q(main_challenge__end_date__gt=datetime.datetime.now()) | Q(main_challenge__end_date__isnull=True))


class BaseChallengeViewSet(viewsets.ModelViewSet):
    """A viewset to extend for all other challenge types"""
    http_method_names = ('get', 'head', 'options')


class ArticleChallengeViewSet(BaseChallengeViewSet):
    """
    A viewset for Article challenges.
    """
    serializer_class = ArticleChallengeSerializer
    queryset = ArticleChallenge.objects.filter(
        query_challenge_visible
    )


class EventParticipantChallengeViewSet(BaseChallengeViewSet):
    """
    A ViewSet for EventParticipant challenges.
    """
    serializer_class = EventParticipantChallengeSerializer
    queryset = EventParticipantChallenge.objects.filter(
        query_challenge_visible
    )


class SchoolGSAChallengeViewSet(BaseChallengeViewSet):
    """
    A ViewSet for SchoolGSA challenges.
    """
    serializer_class = SchoolGSAChallengeSerializer
    queryset = SchoolGSAChallenge.objects.filter(
        query_challenge_visible
    )


class EventOrganizerChallengeViewSet(BaseChallengeViewSet):
    """
    A ViewSet for EventOrganizer challenges.
    """
    serializer_class = EventOrganizerChallengeSerializer
    queryset = EventOrganizerChallenge.objects.filter(
        query_challenge_visible
    )


class StoryChallengeViewSet(BaseChallengeViewSet):
    """
    A ViewSet for Story challenges.
    """
    serializer_class = StoryChallengeSerializer
    queryset = StoryChallenge.objects.filter(
        query_challenge_visible
    )


class ProjectChallengeViewSet(BaseChallengeViewSet):
    """
    A ViewSet for Project challenges.
    """
    serializer_class = ProjectChallengeSerializer
    queryset = ProjectChallenge.objects.filter(
        query_challenge_visible
    )


class ReactingChallengeViewSet(BaseChallengeViewSet):
    """
    A ViewSet for Reacting challenges.
    """
    serializer_class = ReactingChallengeSerializer
    queryset = ReactingChallenge.objects.filter(
        query_challenge_visible
    )


class SupportChallengeViewSet(BaseChallengeViewSet):
    """
    A ViewSet for Support challenges.
    """
    serializer_class = SupportChallengeSerializer
    queryset = SupportChallenge.objects.filter(
        query_challenge_visible
    )


class QuizChallengeViewSet(BaseChallengeViewSet):
    """
    A ViewSet for Quiz challenges.
    """
    serializer_class = QuizChallengeSerializer
    queryset = SupportChallenge.objects.filter(
        query_challenge_visible
    )


class CustomChallengeViewSet(BaseChallengeViewSet):
    """
    A ViewSet for Custom challenges.
    """
    serializer_class = CustomChallengeSerializer
    queryset = CustomChallenge.objects.filter(
        query_challenge_visible
    )
