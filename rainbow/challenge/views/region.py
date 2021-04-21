from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from challenge.models import Region
from challenge.serializers.region import RegionSerializer


class RegionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
