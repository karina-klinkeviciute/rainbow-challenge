import datetime

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from joined_challenge.models import (
    EventOrganizerJoinedChallenge,
    SupportJoinedChallenge,
    JoinedChallenge,
    ArticleJoinedChallenge,
    EventParticipantJoinedChallenge,
    SchoolGSAJoinedChallenge,
    StoryJoinedChallenge,
    ProjectJoinedChallenge,
    ReactingJoinedChallenge,
    CustomJoinedChallenge,
    QuizJoinedChallenge,
)
from joined_challenge.models.base import JoinedChallengeStatus
from quiz.models import QuizUser


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
        status = main_joined_challenge_data["status"]
        if status == JoinedChallengeStatus.CONFIRMED:
            raise serializers.ValidationError(_("Status can't be 'confirmed'"))
        if status == JoinedChallengeStatus.COMPLETED:
            main_joined_challenge.completed_at = datetime.datetime.now()
            if main_joined_challenge.challenge.needs_confirmation is False:
                status = JoinedChallengeStatus.CONFIRMED
                main_joined_challenge.status = status
            main_joined_challenge.save()

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


class SupportJoinedChallengeSerializer(BaseJoinedChallengeSerializer):

    class Meta:
        model = SupportJoinedChallenge
        fields = '__all__'


class CustomJoinedChallengeSerializer(BaseJoinedChallengeSerializer):

    class Meta:
        model = CustomJoinedChallenge
        fields = '__all__'


class QuizJoinedChallengeSerializer(BaseJoinedChallengeSerializer):

    class Meta:
        model = QuizJoinedChallenge
        fields = '__all__'

    def create(self, validated_data):
        this_challenge = super().create(validated_data)
        user = this_challenge.user
        quiz = this_challenge.main_joined_challenge.quiz_challenge.quiz
        quiz_user = QuizUser(user=user, quiz=quiz)
        quiz_user.save()
        this_challenge.quiz_user = quiz_user
        this_challenge.save()
