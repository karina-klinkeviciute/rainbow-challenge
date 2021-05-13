from rest_framework import serializers

from challenge.models import SupportChallenge
from challenge.models.challenge import Challenge, ArticleChallenge, EventParticipantChallenge, ChallengeType
from challenge.models.challenge.event_organizer import EventOrganizerChallenge
from challenge.models.challenge.project import ProjectChallenge
from challenge.models.challenge.reacting import ReactingChallenge
from challenge.models.challenge.school_gsa import SchoolGSAChallenge
from challenge.models.challenge.story import StoryChallenge


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


class SchoolGSAChallengeSerializer(BaseChallengeSerializer):

    class Meta:
        model = SchoolGSAChallenge
        fields = '__all__'


class EventOrganizerChallengeSerializer(BaseChallengeSerializer):

    class Meta:
        model = EventOrganizerChallenge
        fields = '__all__'


class StoryChallengeSerializer(BaseChallengeSerializer):

    class Meta:
        model = StoryChallenge
        fields = '__all__'


class ProjectChallengeSerializer(BaseChallengeSerializer):

    class Meta:
        model = ProjectChallenge
        fields = '__all__'


class ReactingChallengeSerializer(BaseChallengeSerializer):

    class Meta:
        model = ReactingChallenge
        fields = '__all__'


class SupportChallengeSerializer(BaseChallengeSerializer):

    class Meta:
        model = SupportChallenge
        fields = '__all__'