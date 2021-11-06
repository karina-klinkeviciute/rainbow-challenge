# Create your views here.
from rest_framework import views
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from results.models.prize import ClaimedPrize
from results.serializers.prize import ClaimedPrizeSerializer
from user.models import GenderOptions
from user.serializers import GenderSerializer


class GenderListView(views.APIView):
    http_method_names = ('get', )
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get(self, request, format=None):
        genders = GenderOptions()
        serializer = GenderSerializer(genders)
        return Response(serializer.data)


class UserClaimedPrizeAPIView(ListAPIView):
    serializer_class = ClaimedPrizeSerializer

    def get_queryset(self):
        queryset = ClaimedPrize.objects.all()
        user = self.kwargs.get('user_uuid')
        if user is not None:
            queryset = queryset.filter(user=user)
        return queryset
