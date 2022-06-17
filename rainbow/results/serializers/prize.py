from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from results.models.prize import ClaimedPrize, Prize


class PrizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prize
        fields = ['name', 'uuid', 'description', 'amount', 'price', 'amount_remaining', 'image', ]


class ClaimedPrizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClaimedPrize
        fields = ['uuid', 'amount', 'prize', 'issued']
        read_only_fields = ['issued', ]

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data["user"] = user
        return super().create(validated_data)

    def validate(self, data):
        data = super().validate(data)
        amount = data["amount"]
        prize = data["prize"]
        amount_remaining = prize.amount_remaining
        if amount_remaining < amount:
            raise serializers.ValidationError(_("Sorry, we don't have that much of this prize."))
        # todo write tests for this

        cost_points = prize.price * amount
        user = self.context['request'].user
        if user.remaining_points < cost_points:
            raise serializers.ValidationError(_("Sorry, you don't have enough rainbows for that."))

        return data
