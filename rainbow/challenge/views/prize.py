from rest_framework import viewsets

from challenge.models import Prize
from challenge.models.prize import ClaimedPrize
from challenge.serializers.prize import PrizeSerializer, ClaimedPrizeSerializer


class PrizeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = PrizeSerializer
    queryset = Prize.objects.all()


class ClaimedPrizeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = ClaimedPrizeSerializer
    queryset = ClaimedPrize.objects.all()

