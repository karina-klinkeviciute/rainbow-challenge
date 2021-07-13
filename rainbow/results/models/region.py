from django.db import models
import uuid

from joined_challenge.models.base import JoinedChallengeStatus


class Region(models.Model):
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(
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
            status=JoinedChallengeStatus.COMPLETED)

        points = 0

        for completed_challenge in completed_joined_challenges_region:
            points += completed_challenge.challenge.points

        return points
