from rest_framework import viewsets


from challenge.models import (
    JoinedChallenge,
    ArticleJoinedChallenge,
    EventParticipantJoinedChallenge, EventOrganizerJoinedChallenge)
from challenge.models.joined_challenge.school_gsa import SchoolGSAJoinedChallenge
from challenge.serializers.joined_challenge import (
    JoinedChallengeSerializer,
    ArticleJoinedChallengeSerializer,
    EventParticipantJoinedChallengeSerializer, SchoolGSAJoinedChallengeSerializer,
    EventOrganizerJoinedChallengeSerializer)


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
