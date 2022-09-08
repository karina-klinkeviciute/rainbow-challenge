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
            status=JoinedChallengeStatus.CONFIRMED
        )

        points = 0
        for completed_challenge in completed_joined_challenges_region:
            points += completed_challenge.final_points

        return points
