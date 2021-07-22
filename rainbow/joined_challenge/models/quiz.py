from django.db import models
from django.utils.translation import gettext_lazy as _

from joined_challenge.models.base import BaseJoinedChallenge
from quiz.models import QuizUser


class QuizJoinedChallenge(BaseJoinedChallenge):

    quiz_user = models.OneToOneField(
        QuizUser,
        verbose_name=_('quiz user object'),
        on_delete=models.CASCADE,
        null=True
    )

    @property
    def concrete_challenge(self):
        from challenge.models import CustomChallenge
        return CustomChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)

    # todo method for returning the quizuser object or other info from that model
