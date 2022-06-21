from rest_framework import serializers

from challenge.models import SupportChallenge, ArticleChallenge, EventParticipantChallenge
from challenge.models.base import Challenge, ChallengeType
from challenge.models.custom import CustomChallenge
from challenge.models.event_organizer import EventOrganizerChallenge
from challenge.models.project import ProjectChallenge
from challenge.models.quiz import QuizChallenge, Answer, Question
from challenge.models.reacting import ReactingChallenge
from challenge.models.school_gsa import SchoolGSAChallenge
from challenge.models.story import StoryChallenge
from joined_challenge.models import JoinedChallenge
from joined_challenge.models.base import JoinedChallengeStatus


class ChallengeSerializer(serializers.ModelSerializer):
    concrete_challenge_uuid = serializers.UUIDField()
    can_be_joined = serializers.SerializerMethodField()
    concrete_joined_challenges = serializers.SerializerMethodField()
    is_joined = serializers.SerializerMethodField()

    class Meta:
        model = Challenge
        fields = ('uuid',
                  'type',
                  'name',
                  'description',
                  'image',
                  'points',
                  'region',
                  'start_date',
                  'end_date',
                  'multiple',
                  'needs_confirmation',
                  'concrete_challenge_uuid',
                  'can_be_joined',
                  'concrete_joined_challenges',
                  'is_joined'
                  )

    def get_can_be_joined(self, obj):
        """
        Checks if the current user can join this challenge
        Users can't join challenges which are not multiple and they have already joined it.
        """
        if obj.multiple is False:
            user = self.context["request"].user
            joined_challenges = JoinedChallenge.objects.filter(challenge=obj, user=user)
            if len(joined_challenges) > 0:
                return False
            return True
        return True

    def get_concrete_joined_challenges(self, obj):
        """
        returns a list of User's joined challenges
        """
        request = self.context.get("request")
        user = request.user
        joined_challenges = JoinedChallenge.objects.filter(
            challenge=obj, user=user, status=JoinedChallengeStatus.JOINED
        )
        concrete_joined_challenges = list()
        for joined_challenge in joined_challenges:
            concrete_joined_challenges.append(
                {
                    "uuid": joined_challenge.concrete_joined_challenge,
                    "date_joined": joined_challenge.joined_at.date(),
                    "main_joined_challenge": joined_challenge.uuid,
                    # "files": joined_challenge.files.values_list('file', flat=True),
                    "files": [
                        {
                            "uuid": file.uuid,
                            "file_name": str(file.file).split("/")[-1],
                            "file_url": request.build_absolute_uri("/") + 'private-media/' + str(file.file)
                        } for file in joined_challenge.files.all()
                    ]
                }
            )
        return concrete_joined_challenges

    def get_is_joined(self, obj):
        user = self.context["request"].user
        joined_challenges = JoinedChallenge.objects.filter(
            challenge=obj, user=user, status=JoinedChallengeStatus.JOINED
        )
        if len(joined_challenges) > 0:
            return True
        else:
            return False


class BaseChallengeSerializer(serializers.ModelSerializer):
    main_challenge = ChallengeSerializer()


class ArticleChallengeSerializer(BaseChallengeSerializer):

    class Meta:
        model = ArticleChallenge
        fields = '__all__'


class EventParticipantChallengeSerializer(BaseChallengeSerializer):

    class Meta:
        model = EventParticipantChallenge
        fields = ('uuid', 'main_challenge', 'event_name', 'date', 'url')


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


class CustomChallengeSerializer(BaseChallengeSerializer):

    class Meta:
        model = CustomChallenge
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('uuid', 'answer')


class QuestionSerializer(serializers.ModelSerializer):

    answers = serializers.SerializerMethodField()
    is_answered = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('uuid', 'question', 'answers', 'is_answered', )
        read_only_fields = ('is_answered', )

    def get_is_answered(self, obj):
        request = self.context.get("request")
        user = request.user
        from joined_challenge.models.quiz import UserAnswer
        if UserAnswer.objects.filter(
                quiz_joined_challenge__main_joined_challenge__user=user,
                answer__question=obj
        ).exists():
            return True
        return False

    def get_answers(self, obj):
        answers = Answer.objects.filter(question=obj)
        return AnswerSerializer(answers, many=True).data


class QuizChallengeSerializer(BaseChallengeSerializer):

    questions = serializers.SerializerMethodField()

    class Meta:
        model = QuizChallenge
        fields = ('main_challenge', 'questions')

    def get_questions(self, obj):
        questions = Question.objects.filter(quiz=obj)
        questions_filtered = []
        request = self.context.get("request")
        user = request.user
        from joined_challenge.models.quiz import UserAnswer
        for question in questions:
            if not UserAnswer.objects.filter(
                    quiz_joined_challenge__main_joined_challenge__user=user,
                    answer__question=question
            ).exists():
                questions_filtered.append(question)
        return QuestionSerializer(questions_filtered, many=True, context=self.context).data
