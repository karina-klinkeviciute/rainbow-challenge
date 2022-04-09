import datetime

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from results.models.prize import ClaimedPrize, Prize
from results.serializers.prize import PrizeSerializer, ClaimedPrizeSerializer


class PrizeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing prizes.
    """
    http_method_names = ('get', 'head', 'options')
    serializer_class = PrizeSerializer
    queryset = Prize.objects.all()


class AvailablePrizeViewSet(viewsets.ModelViewSet):
    """A view for only available prizes"""
    http_method_names = ('get', 'head', 'options')
    serializer_class = PrizeSerializer

    def get_queryset(self):
        """We only need those prizes that are available"""
        prizes = Prize.objects.filter(

            Q(
                expires_at__gt=datetime.datetime.today()) | Q(expires_at__isnull=True),
                available=True
              )

        prizes = (prize for prize in prizes if prize.amount_remaining > 0)
        return prizes


class ClaimedPrizeViewSet(viewsets.ModelViewSet):
    """Prizes that are claimed by users"""
    http_method_names = ('get', 'post', 'head', 'options')
    serializer_class = ClaimedPrizeSerializer

    def get_queryset(self):
        queryset = ClaimedPrize.objects.filter(user=self.request.user)
        return queryset
