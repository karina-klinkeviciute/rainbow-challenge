from django.db import models
from django.utils.translation import gettext_lazy as _

from joined_challenge.models.base import BaseJoinedChallenge


class CustomJoinedChallenge(BaseJoinedChallenge):
    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
        null=True
    )

    @property
    def concrete_challenge(self):
        from challenge.models import CustomChallenge
        return CustomChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)
