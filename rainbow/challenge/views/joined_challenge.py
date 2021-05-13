from rest_framework import viewsets


from challenge.models import (
    JoinedChallenge,
    ArticleJoinedChallenge,
    EventParticipantJoinedChallenge, EventOrganizerJoinedChallenge)
from challenge.models.joined_challenge.project import ProjectJoinedChallenge
from challenge.models.joined_challenge.reacting import ReactingJoinedChallenge
from challenge.models.joined_challenge.school_gsa import SchoolGSAJoinedChallenge
from challenge.models.joined_challenge.story import StoryJoinedChallenge
from challenge.serializers.joined_challenge import (
    JoinedChallengeSerializer,
    ArticleJoinedChallengeSerializer,
    EventParticipantJoinedChallengeSerializer, SchoolGSAJoinedChallengeSerializer,
    EventOrganizerJoinedChallengeSerializer, StoryJoinedChallengeSerializer, ProjectJoinedChallengeSerializer,
    ReactingJoinedChallengeSerializer)


class JoinedChallengeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = JoinedChallengeSerializer
    queryset = JoinedChallenge.objects.all()


class ArticleJoinedChallengeViewSet(viewsets.ModelViewSet):
    """
    A viewset for Article challenges.
    """
    serializer_class = ArticleJoinedChallengeSerializer
    queryset = ArticleJoinedChallenge.objects.all()


class EventParticipantJoinedChallengeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for EventParticipant challenges.
    """
    serializer_class = EventParticipantJoinedChallengeSerializer
    queryset = EventParticipantJoinedChallenge.objects.all()


class SchoolGSAJoinedChallengeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for SchoolGSA challenges.
    """
    serializer_class = SchoolGSAJoinedChallengeSerializer
    queryset = SchoolGSAJoinedChallenge.objects.all()


class EventOrganizerJoinedChallengeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for EventOrganizer challenges.
    """
    serializer_class = EventOrganizerJoinedChallengeSerializer
    queryset = EventOrganizerJoinedChallenge.objects.all()


class StoryJoinedChallengeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for EventOrganizer challenges.
    """
    serializer_class = StoryJoinedChallengeSerializer
    queryset = StoryJoinedChallenge.objects.all()


class ProjectJoinedChallengeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for EventOrganizer challenges.
    """
    serializer_class = ProjectJoinedChallengeSerializer
    queryset = ProjectJoinedChallenge.objects.all()


class ReactingJoinedChallengeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for EventOrganizer challenges.
    """
    serializer_class = ReactingJoinedChallengeSerializer
    queryset = ReactingJoinedChallenge.objects.all()
