from rest_framework import serializers

from challenge.models import Prize


class PrizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prize
        fields = ['name', 'uuid', 'description', 'amount']
