from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from results.models import Medal


class MedalSerializer(serializers.ModelSerializer):
    """Serializer for Medal model"""
    class Meta:
        model = Medal
        fields = ("level", "time_issued")
        