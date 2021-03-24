from django.db import models
import uuid

from django.db.models import Sum

from challenge.models.joined_challenge import JoinedChallengeStatus


class Region(models.Model):
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False)

    def points(self):
        from challenge.models import Challenge
        return Challenge.objects.filter(
            joinedchallenge__user__in=self.user_set,
            joinedchallenge__status=JoinedChallengeStatus.COMPLETED).aggregate(Sum('points'))
