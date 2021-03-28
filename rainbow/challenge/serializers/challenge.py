from rest_framework import serializers

from challenge.models.challenge import Challenge, ArticleChallenge, EventParticipantChallenge, ChallengeType


class ChallengeSerializer(serializers.ModelSerializer):
    concrete_challenge_uuid = serializers.UUIDField()

    class Meta:
        model = Challenge
        fields = '__all__'


class BaseChallengeSerializer(serializers.ModelSerializer):
    main_challenge = ChallengeSerializer()


class ArticleChallengeSerializer(BaseChallengeSerializer):

    class Meta:
        model = ArticleChallenge
        fields = '__all__'


class EventParticipantChallengeSerializer(BaseChallengeSerializer):

    class Meta:
        model = EventParticipantChallenge
        fields = '__all__'
