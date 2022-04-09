import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from challenge.models.base import BaseChallenge


class QuizChallenge(BaseChallenge):
    """Article challenge"""
    pass


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
        QuizChallenge,
        verbose_name=_('quiz'),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.question


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

    def __str__(self):
        return self.answer
