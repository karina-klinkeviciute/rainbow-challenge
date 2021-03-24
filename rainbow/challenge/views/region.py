from rest_framework import viewsets

from challenge.models import Region
from challenge.serializers.region import RegionSerializer


class RegionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = RegionSerializer
    queryset = Region.objects.all()
