from django.db import models
import uuid

from django.db.models import Sum

from challenge.models.joined_challenge import JoinedChallengeStatus, JoinedChallenge


class Region(models.Model):
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False)

    def __str__(self):
        return self.name

    @property
    def points(self):
        from challenge.models import Challenge
        joined_joined_challenges_region = JoinedChallenge.objects.filter(
            user__in=self.user_set.all())

        completed_joined_challenges_region = joined_joined_challenges_region.filter(
            status=JoinedChallengeStatus.COMPLETED)

        points = 0

        for completed_challenge in completed_joined_challenges_region:
            points += completed_challenge.challenge.points

        return points
