from django.db import models
from django.utils.translation import gettext_lazy as _

from joined_challenge.models.base import BaseJoinedChallenge


class SupportJoinedChallenge(BaseJoinedChallenge):
    description = models.TextField(
        verbose_name=_('description of support'),
        blank=True,
        null=True
    )

    @property
    def concrete_challenge(self):
        from challenge.models.support import SupportChallenge
        return SupportChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)
