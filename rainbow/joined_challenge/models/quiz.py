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
        return UserAnswer.objects.filter(answer__correct=True).count()
#     TODO check if correct

   # @property
   #  def all_answered(self):
   #      """If amount of answered questions is the same as all questions, it's completed"""
   #      quiz_questions = self.main_joined_challenge.challengequestion_set
   #      quiz_answers = Answer.objects.filter(question__in=quiz_questions)
   #      quiz_user_answers = self.useranswer_set
   #      if quiz_answers.count() == quiz_user_answers.count():
   #          return True
   #      else:
   #          return False


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
