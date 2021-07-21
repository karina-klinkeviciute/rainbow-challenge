from django.db import models
from django.utils.translation import gettext_lazy as _

from challenge.models.base import BaseChallenge
from quiz.models import Quiz


class QuizChallenge(BaseChallenge):
    """Article challenge"""
    quiz = models.OneToOneField(
        Quiz,
        on_delete=models.DO_NOTHING,
        verbose_name=_('quiz')
    )
