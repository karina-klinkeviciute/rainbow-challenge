from rest_framework import serializers

from challenge.models.joined_challenge import JoinedChallenge, ArticleJoinedChallenge, EventParticipantJoinedChallenge


class JoinedChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinedChallenge
        fields = '__all__'


class BaseJoinedChallengeSerializer(serializers.ModelSerializer):
    main_joined_challenge = JoinedChallengeSerializer()


class ArticleJoinedChallengeSerializer(BaseJoinedChallengeSerializer):

    class Meta:
        model = ArticleJoinedChallenge
        fields = '__all__'


class EventParticipantJoinedChallengeSerializer(BaseJoinedChallengeSerializer):

    class Meta:
        model = EventParticipantJoinedChallenge
        fields = '__all__'
