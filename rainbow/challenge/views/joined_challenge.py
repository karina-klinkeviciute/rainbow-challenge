from rest_framework import viewsets


from challenge.models.joined_challenge import (
    JoinedChallenge,
    ArticleJoinedChallenge,
    EventParticipantJoinedChallenge)
from challenge.serializers.joined_challenge import (
    JoinedChallengeSerializer,
    ArticleJoinedChallengeSerializer,
    EventParticipantJoinedChallengeSerializer)


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
