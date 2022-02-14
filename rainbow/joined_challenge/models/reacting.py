from django.db import models
from django.utils.translation import gettext_lazy as _

from joined_challenge.models.base import BaseJoinedChallenge


class ReactingJoinedChallenge(BaseJoinedChallenge):
    description = models.TextField(
        verbose_name=_('description of the reaction in your own words'),
        blank=True,
        null=True
    )

    @property
    def concrete_challenge(self):
        from challenge.models.reacting import ReactingChallenge
        return ReactingChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)
