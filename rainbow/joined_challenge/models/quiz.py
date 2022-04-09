import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from challenge.models.quiz import Answer
from joined_challenge.models.base import BaseJoinedChallenge


class QuizJoinedChallenge(BaseJoinedChallenge):

    @property
    def concrete_challenge(self):
        from challenge.models import QuizChallenge
        return QuizChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)


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
    quiz_joined_challenge = models.ForeignKey(
        QuizJoinedChallenge,
        verbose_name=_("quiz joined challenge"),
        on_delete=models.CASCADE
    )

    @property
    def is_correct(self):
        return self.answer.correct

