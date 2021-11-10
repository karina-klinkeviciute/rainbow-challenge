from django.db import models
from django.utils.translation import gettext_lazy as _

from joined_challenge.models.base import BaseJoinedChallenge


class EventParticipantJoinedChallenge(BaseJoinedChallenge):
    """Class for a challenge for participation in an event"""

    qr_code = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("QR code")
    )

    @property
    def concrete_challenge(self):
        from challenge.models import EventParticipantChallenge
        return EventParticipantChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)
