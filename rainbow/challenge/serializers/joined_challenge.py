from rest_framework import serializers

from challenge.models.joined_challenge import JoinedChallenge, ArticleJoinedChallenge, EventParticipantJoinedChallenge


class JoinedChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinedChallenge
        fields = '__all__'


class BaseJoinedChallengeSerializer(serializers.ModelSerializer):
    main_joined_challenge = JoinedChallengeSerializer()

    def create(self, validated_data):
        main_joined_challenge_data = validated_data.pop('main_joined_challenge')
        this_challenge = self.Meta.model.objects.create(**validated_data)
        main_joined_challenge = JoinedChallenge.objects.create(**main_joined_challenge_data)
        this_challenge.main_joined_challenge = main_joined_challenge
        this_challenge.save()
        return this_challenge

    def update(self, instance, validated_data):
        main_joined_challenge_data = validated_data.pop('main_joined_challenge')
        this_challenge = instance
        main_joined_challenge = instance.main_joined_challenge
        this_challenge.main_joined_challenge = main_joined_challenge
        this_challenge.save()
        return this_challenge


class ArticleJoinedChallengeSerializer(BaseJoinedChallengeSerializer):

    class Meta:
        model = ArticleJoinedChallenge
        fields = '__all__'


class EventParticipantJoinedChallengeSerializer(BaseJoinedChallengeSerializer):

    class Meta:
        model = EventParticipantJoinedChallenge
        fields = '__all__'
