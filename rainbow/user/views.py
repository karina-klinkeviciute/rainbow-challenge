from django.shortcuts import render

# Create your views here.
from rest_framework import views
from rest_framework.response import Response

from user.models import GenderOptions
from user.serializers import GenderSerializer


class GenderListView(views.APIView):
    def get(self, request, format=None):
        genders = GenderOptions()
        serializer = GenderSerializer(genders)
        return Response(serializer.data)
