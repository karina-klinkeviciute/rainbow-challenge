from django.db import models
from django.utils.translation import gettext_lazy as _

from challenge.models.challenge.event_organizer import EventOrganizerChallenge
from challenge.models.challenge.reacting import ReactingChallenge
from challenge.models.joined_challenge.base import BaseJoinedChallenge


class ReactingJoinedChallenge(BaseJoinedChallenge):
    reaction_description = models.TextField(
        verbose_name=_('description of the reaction in your own words')
    )

    @property
    def concrete_challenge(self):
        return ReactingChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)
