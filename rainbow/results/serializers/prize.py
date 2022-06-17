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

        # prize = validated_data.pop('main_joined_challenge')

        # Check if this user can join this challenge.
        # User can't join challenge if they have already done it and the challenge isn't 'multiple'
        # challenge = main_joined_challenge_data['challenge']
        user = self.context['request'].user
        validated_data["user"] = user
        return super().create(validated_data)
        # main_joined_challenge_data["user"] = user
        # if challenge.multiple is False:
        #     if JoinedChallenge.objects.filter(challenge=challenge, user=user).exists():
        #         raise serializers.ValidationError(_("This challenge can be joined only once."))
        #
        # this_challenge = self.Meta.model.objects.create(**validated_data)
        #
        # main_joined_challenge = JoinedChallenge.objects.create(**main_joined_challenge_data)
        # main_joined_challenge.save()
        # this_challenge.main_joined_challenge = main_joined_challenge
        # this_challenge.save()
        # return this_challenge

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
