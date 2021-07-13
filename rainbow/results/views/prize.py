from rest_framework import viewsets

from results.models.prize import ClaimedPrize, Prize
from results.serializers.prize import PrizeSerializer, ClaimedPrizeSerializer


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

