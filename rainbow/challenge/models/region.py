from django.db import models
import uuid

from django.db.models import Sum

from challenge.models.joined_challenge import JoinedChallengeStatus


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
        all_challenges_region = Challenge.objects.filter(
            joinedchallenge__user__in=self.user_set.all())

        completed_challenges_region = all_challenges_region.filter(
            joinedchallenge__status=JoinedChallengeStatus.COMPLETED)

        points = completed_challenges_region.aggregate(Sum('points', distinct=True))
        # print(points.query)

        return points['points__sum']
