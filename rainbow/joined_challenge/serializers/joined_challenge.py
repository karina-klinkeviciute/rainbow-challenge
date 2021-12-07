from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from challenge.models import EventParticipantChallenge
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
from joined_challenge.models.base import JoinedChallengeStatus, JoinedChallengeFile
from quiz.models import QuizUser


class JoinedChallengeFileSerializer(serializers.ModelSerializer):
    """Serializer for files added to joined challenges. """
    class Meta:
        model = JoinedChallengeFile
        fields = ('uuid', 'joined_challenge', 'file')


class JoinedChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinedChallenge
        fields = ('uuid', 'status', 'challenge', 'concrete_joined_challenge', 'challenge_type', 'files', )

    files = JoinedChallengeFileSerializer(many=True, read_only=True)


class BaseJoinedChallengeSerializer(serializers.ModelSerializer):
    main_joined_challenge = JoinedChallengeSerializer()

    def create(self, validated_data):

        main_joined_challenge_data = validated_data.pop('main_joined_challenge')

        # Check if this user can join this challenge.
        # User can't join challenge if they have already done it and the challenge isn't 'multiple'
        challenge = main_joined_challenge_data['challenge']
        user = self.context['request'].user
        main_joined_challenge_data["user"] = user
        if challenge.multiple is False:
            if JoinedChallenge.objects.filter(challenge=challenge, user=user).exists():
                raise serializers.ValidationError(_("This challenge can be joined only once."))

        this_challenge = self.Meta.model.objects.create(**validated_data)

        main_joined_challenge = JoinedChallenge.objects.create(**main_joined_challenge_data)
        main_joined_challenge.save()
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
        # fields = ('main_joined_challenge', 'qr_code', 'concrete_challenge')
        fields = '__all__'

    def validate_qr_code(self, value):
        challenge_uuid = self.initial_data["main_joined_challenge"]["challenge"]
        event_challenge = EventParticipantChallenge.objects.get(main_challenge__uuid=challenge_uuid)
        challenge_qr_code = event_challenge.qr_code
        if value != challenge_qr_code:
            raise serializers.ValidationError(_("QR code is invalid."))
        return value


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


