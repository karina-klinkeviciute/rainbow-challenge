from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from challenge.models import Challenge
from challenge.serializers.challenge import ChallengeSerializer
from results.models.region import Region
from results.serializers.region import RegionSerializer
from user.serializers import UserSerializer

from user.models import User


class RegionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    serializer_class = RegionSerializer
    queryset = Region.objects.all()


class RegionUsersAPIView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        region = self.kwargs.get('region_uuid')
        if region is not None:
            queryset = queryset.filter(region=region)
        return queryset


class RegionChallengesAPIView(ListAPIView):
    serializer_class = ChallengeSerializer

    def get_queryset(self):
        queryset = Challenge.active.all()
        region = self.kwargs.get('region_uuid')
        if region is not None:
            queryset = queryset.filter(region=region)
        return queryset
