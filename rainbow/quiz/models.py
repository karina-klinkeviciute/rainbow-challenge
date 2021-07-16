import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Quiz (models.Model):
    """A class for quiz"""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    name = models.CharField(
        verbose_name=_('name'),
        max_length=1000)
    description = models.TextField(
        verbose_name=_('description'),
        null=True,
        blank=True
    )


class QuizUser(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name=_('quiz')
    )
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        verbose_name=_('user')
    )

    def evaluate_quiz(self):
        pass
#         todo finish this


class Question(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    question = models.TextField(
        verbose_name=_('question')
    )
    quiz = models.ForeignKey(
        Quiz,
        verbose_name=_('question'),
        on_delete=models.CASCADE
    )


class Answer(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    answer = models.TextField(
        verbose_name=_('answer')
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name=_('question')
    )
    correct = models.BooleanField(
        verbose_name=_('correct answer'),
        default=False
    )


class UserAnswer(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        verbose_name=_('answer')
    )
    quiz_user = models.ForeignKey(
        QuizUser,
        on_delete=models.CASCADE,
        verbose_name=_("quiz-user connection")
    )
