import datetime

from django.db.models import Q
from rest_framework import viewsets


from challenge.models.challenge import Challenge, ArticleChallenge, EventParticipantChallenge
from challenge.serializers.challenge import ChallengeSerializer, ArticleChallengeSerializer, \
    EventParticipantChallengeSerializer


class ChallengeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = ChallengeSerializer
    queryset = Challenge.objects.filter(
        Q(published=True),
        Q(start_date__lt=datetime.datetime.now()) | Q(start_date__isnull=True),
        Q(end_date__gt=datetime.datetime.now()) | Q(end_date__isnull=True)
    )


class ArticleChallengeViewSet(viewsets.ModelViewSet):
    """
    A viewset for Article challenges.
    """
    serializer_class = ArticleChallengeSerializer
    queryset = ArticleChallenge.objects.all()


class EventParticipantChallengeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for EventParticipant challenges.
    """
    serializer_class = EventParticipantChallengeSerializer
    queryset = EventParticipantChallenge.objects.all()
