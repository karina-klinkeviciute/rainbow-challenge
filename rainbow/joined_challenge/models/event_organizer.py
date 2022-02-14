from django.db import models
from django.utils.translation import gettext_lazy as _

from joined_challenge.models.base import BaseJoinedChallenge


class EventOrganizerJoinedChallenge(BaseJoinedChallenge):
    event_name = models.TextField(
        verbose_name=_("name of the event"),
        blank=True,
        null=True
    )
    event_url = models.URLField(
        verbose_name=_('link to the event website or Facebook page if there is one'),
        blank=True,
        null=True
    )
    description = models.TextField(
        verbose_name=_('description of the event in your own words'),
        blank=True,
        null=True
    )
    organized_alone = models.BooleanField(
        verbose_name=_('was this event was organized by you alone'),
        blank=True,
        null=True
    )

    @property
    def concrete_challenge(self):
        from challenge.models.event_organizer import EventOrganizerChallenge
        return EventOrganizerChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)
