from rest_framework import serializers

from challenge.models import EventOrganizerJoinedChallenge
from challenge.models.joined_challenge import JoinedChallenge, ArticleJoinedChallenge, EventParticipantJoinedChallenge
from challenge.models.joined_challenge.project import ProjectJoinedChallenge
from challenge.models.joined_challenge.reacting import ReactingJoinedChallenge
from challenge.models.joined_challenge.school_gsa import SchoolGSAJoinedChallenge
from challenge.models.joined_challenge.story import StoryJoinedChallenge


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


class SchoolGSAJoinedChallengeSerializer(BaseJoinedChallengeSerializer):

    class Meta:
        model = SchoolGSAJoinedChallenge
        fields = '__all__'


class EventOrganizerJoinedChallengeSerializer(BaseJoinedChallengeSerializer):

    class Meta:
        model = EventOrganizerJoinedChallenge
        fields = '__all__'


class StoryJoinedChallengeSerializer(BaseJoinedChallengeSerializer):

    class Meta:
        model = StoryJoinedChallenge
        fields = '__all__'


class ProjectJoinedChallengeSerializer(BaseJoinedChallengeSerializer):

    class Meta:
        model = ProjectJoinedChallenge
        fields = '__all__'


class ReactingJoinedChallengeSerializer(BaseJoinedChallengeSerializer):

    class Meta:
        model = ReactingJoinedChallenge
        fields = '__all__'