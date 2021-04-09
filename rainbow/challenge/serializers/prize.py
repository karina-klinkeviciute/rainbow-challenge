from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from challenge.models import Prize
from challenge.models.prize import ClaimedPrize


class PrizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prize
        fields = ['name', 'uuid', 'description', 'amount', 'price', 'amount_remaining', ]


class ClaimedPrizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClaimedPrize
        fields = ['user', 'uuid', 'amount', 'prize', ]

    def validate(self, data):
        data = super().validate(data)
        amount = data["amount"]
        prize = data["prize"]
        amount_remaining = prize.amount_remaining
        if amount_remaining < amount:
            raise serializers.ValidationError(_("Sorry, we don't have that much of this prize."))
        # todo write tests for this
        return data
