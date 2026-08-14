import datetime

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from results.models.prize import ClaimedPrize, Prize
from results.permissions import IsClaimedPrizeOwner
from results.serializers.prize import PrizeSerializer, ClaimedPrizeSerializer


class PrizeViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only catalogue of prizes, visible to any authenticated user.

    The prize catalogue is shared reference data; users may browse it but never
    edit it through the API. Prizes are created/edited only via the Django admin
    (or the staff-only dashboard). Using ``ReadOnlyModelViewSet`` enforces this
    structurally -- there simply are no write routes -- rather than relying on
    ``http_method_names`` to hide them on a full ``ModelViewSet``.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PrizeSerializer
    queryset = Prize.objects.all()


class AvailablePrizeViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only view of only the currently available prizes."""
    permission_classes = [IsAuthenticated]
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
    """Prizes that are claimed by users.

    A user only ever sees and claims their own prizes: the queryset is scoped to
    ``request.user`` (so lists/retrieves never leak other users' claims) and
    ``IsClaimedPrizeOwner`` guards object access as defence-in-depth. Cross-user
    access is reserved for the Django admin, matching the issue #104 contract.
    """
    http_method_names = ('get', 'post', 'head', 'options')
    permission_classes = [IsAuthenticated, IsClaimedPrizeOwner]
    serializer_class = ClaimedPrizeSerializer

    def get_queryset(self):
        queryset = ClaimedPrize.objects.filter(user=self.request.user)
        return queryset
