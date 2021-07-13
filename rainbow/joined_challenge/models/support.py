from django.db import models
from django.utils.translation import gettext_lazy as _

from joined_challenge.models.base import BaseJoinedChallenge


class SupportJoinedChallenge(BaseJoinedChallenge):
    other_organization = models.CharField(
        verbose_name=_('Other organization'),
        help_text=_('only if organization on challenge is Other'),
        max_length=1000,
        null=True,
        blank=True
    )

    @property
    def concrete_challenge(self):
        from challenge.models.support import SupportChallenge
        return SupportChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)
