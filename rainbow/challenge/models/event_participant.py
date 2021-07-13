from django.db import models
from django.utils.translation import gettext_lazy as _

from challenge.models.base import BaseChallenge


class EventParticipantChallenge(BaseChallenge):
    """Event participant challenge is when you
    participate in some event organized by others"""
    event_name = models.CharField(
        max_length=1000,
        verbose_name=_("event name")
    )
    date = models.DateField(
        verbose_name=_("date"),
        null=True,
        blank=True
    )
    # todo is date required?
    url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("link to the event"))
