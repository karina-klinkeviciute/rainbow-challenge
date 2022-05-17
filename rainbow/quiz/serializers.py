from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from quiz.models import Quiz, QuizUser, Question, Answer, UserAnswer


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuizUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizUser
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'
