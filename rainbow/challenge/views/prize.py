from rest_framework import viewsets

from challenge.models import Prize
from challenge.serializers.prize import PrizeSerializer


class PrizeViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = PrizeSerializer
    queryset = Prize.objects.all()
