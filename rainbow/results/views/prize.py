from rest_framework import viewsets

from results.models.prize import ClaimedPrize, Prize
from results.serializers.prize import PrizeSerializer, ClaimedPrizeSerializer


class PrizeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing prizes.
    """
    serializer_class = PrizeSerializer
    queryset = Prize.objects.all()


class AvailablePrizeViewSet(viewsets.ModelViewSet):
    """A view for only available prizes"""
    serializer_class = PrizeSerializer

    def get_queryset(self):
        """We only need those prizes that are """
        prizes = Prize.objects.filter(available=True)
        prizes = (prize for prize in prizes if prize.amount_remaining > 0)
        return prizes


class ClaimedPrizeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing prizes claimed by a user.
    """
    serializer_class = ClaimedPrizeSerializer
    queryset = ClaimedPrize.objects.all()

