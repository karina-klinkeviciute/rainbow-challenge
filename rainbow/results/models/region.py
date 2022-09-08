import uuid

from django.utils.translation import gettext_lazy as _
from django.db import models

from challenge.models.base import ChallengeType
from joined_challenge.models.base import JoinedChallengeStatus


class Region(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=255, unique=True)
    uuid = models.UUIDField(
        verbose_name=_("uuid"),
        default=uuid.uuid4,
        primary_key=True,
        editable=False)

    def __str__(self):
        return self.name

    @property
    def points(self):
        from joined_challenge.models import JoinedChallenge
        joined_joined_challenges_region = JoinedChallenge.objects.filter(
            user__in=self.user_set.all())

        completed_joined_challenges_region = joined_joined_challenges_region.filter(
            status__in=(JoinedChallengeStatus.COMPLETED, JoinedChallengeStatus.CONFIRMED))

        points = 0
        # todo for quiz this is different, change calculation for quiz
        for completed_challenge in completed_joined_challenges_region:
            if completed_challenge.challenge_type == ChallengeType.QUIZ:
                points += completed_challenge.quizjoinedchallenge.correct_answers_count
            else:
                points += completed_challenge.challenge.points

        return points
