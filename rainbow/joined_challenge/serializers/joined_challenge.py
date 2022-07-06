from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from challenge.models import EventParticipantChallenge
from challenge.models.quiz import Answer
from challenge.serializers.challenge import AnswerSerializer
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
from joined_challenge.models.quiz import UserAnswer
from joined_challenge.serializers.files import JoinedChallengeFileSerializer


class JoinedChallengeSerializer(serializers.ModelSerializer):
    from challenge.serializers.challenge import ChallengeSerializer
    challenge_data = ChallengeSerializer(source='challenge', read_only=True)

    class Meta:
        model = JoinedChallenge
        fields = (
            'uuid',
            'status',
            'challenge',
            'challenge_data',
            'concrete_joined_challenge',
            'challenge_type',
            'joined_at',
            'files',
        )

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
        this_challenge = super().update(this_challenge, validated_data)

        return this_challenge


class ArticleJoinedChallengeSerializer(BaseJoinedChallengeSerializer):

    class Meta:
        model = ArticleJoinedChallenge
        fields = '__all__'


class EventParticipantJoinedChallengeSerializer(BaseJoinedChallengeSerializer):

    class Meta:
        model = EventParticipantJoinedChallenge
        fields = '__all__'

    def validate_qr_code(self, value):
        event_challenge = self.instance.main_joined_challenge.challenge.eventparticipantchallenge
        challenge_qr_code = event_challenge.qr_code
        if value != challenge_qr_code:
            raise serializers.ValidationError(_("QR code is invalid."))
        return value


class QRCodeScanSerializer(serializers.Serializer):
    qr_code = serializers.CharField()
    joined_challenge_name = serializers.CharField(read_only=True)
    points = serializers.IntegerField(read_only=True)

    def validate_qr_code(self, value):
        user = self.context.get("user")
        try:
            event_participant_challenge = EventParticipantChallenge.objects.get(qr_code=value)
        except EventParticipantChallenge.DoesNotExist:
            raise serializers.ValidationError(_("QR code is invalid."))

        if EventParticipantJoinedChallenge.objects.filter(
                main_joined_challenge__challenge__eventparticipantchallenge=event_participant_challenge,
                main_joined_challenge__user=user
                ).exists():
            raise serializers.ValidationError(_("You have already completed this challenge"))

        return value

    def create(self, validated_data):
        qr_code = validated_data["qr_code"]
        event_participant_challenge = EventParticipantChallenge.objects.get(qr_code=qr_code)
        user = self.context.get("user")
        event_participant_main_joined_challenge = JoinedChallenge(
            user=user,
            challenge=event_participant_challenge.main_challenge,
            status=JoinedChallengeStatus.CONFIRMED
        )
        event_participant_main_joined_challenge.save()
        event_participant_joined_challenge = EventParticipantJoinedChallenge(
            main_joined_challenge=event_participant_main_joined_challenge,
            qr_code=qr_code
        )
        event_participant_joined_challenge.save()
        data = {
            "qr_code": qr_code,
            "joined_challenge_name": event_participant_challenge.main_challenge.name,
            "points": event_participant_challenge.main_challenge.points}
        return data


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

    correct_answers_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = QuizJoinedChallenge
        fields = ("uuid", "main_joined_challenge", "correct_answers_count")
        read_only_fields = ("correct_answers_count", )


class UserAnswerSerializer(serializers.ModelSerializer):
    correct_answer = AnswerSerializer(read_only=True)

    class Meta:
        model = UserAnswer
        fields = ('uuid', 'answer', 'is_correct', 'correct_answer')
        read_only_fields = ('is_correct', 'correct_answer')

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        answer_uuid = request.data["answer"]
        answer = Answer.objects.get(uuid=answer_uuid)
        question = answer.question
        quiz_challenge = question.quiz
        quiz_joined_challenge = QuizJoinedChallenge.objects.get(
            main_joined_challenge__user=user,
            main_joined_challenge__challenge=quiz_challenge.main_challenge)
        user_answer = UserAnswer(answer=answer, quiz_joined_challenge=quiz_joined_challenge)
        user_answer.save()

        return user_answer

    def validate_answer(self, value):
        answer = Answer.objects.get(uuid=self.initial_data["answer"])
        question = answer.question
        if UserAnswer.objects.filter(answer__question=question).exists():
            raise serializers.ValidationError(_("This question has already been answered."))
        return value

    # TODO overwrite update method to return total points on completion