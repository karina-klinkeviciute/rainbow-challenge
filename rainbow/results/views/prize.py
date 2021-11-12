from rest_framework import viewsets
from rest_framework.generics import ListAPIView

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
        """We only need those prizes that are available"""
        prizes = Prize.objects.filter(available=True)
        prizes = (prize for prize in prizes if prize.amount_remaining > 0)
        return prizes


class UserClaimedPrizesAPIView(ListAPIView):
    serializer_class = ClaimedPrizeSerializer

    def get_queryset(self):
        queryset = ClaimedPrize.objects.all()
        user = self.request.user
        if user is not None:
            queryset = queryset.filter(user=user)
        return queryset
