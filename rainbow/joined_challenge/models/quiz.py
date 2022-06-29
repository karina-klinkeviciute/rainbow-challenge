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

    @property
    def correct_answers_count(self):
        return UserAnswer.objects.filter(answer__correct=True, quiz_joined_challenge=self).count()


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
        on_delete=models.CASCADE,
        verbose_name=_("quiz joined challenge")
    )

    @property
    def is_correct(self):
        return self.answer.correct

    @property
    def correct_answer(self):
        answer = self.answer.question.answer_set.get(correct=True)
        return answer
