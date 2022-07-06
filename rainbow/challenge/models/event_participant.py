import uuid

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
    url = models.URLField(
        blank=True,
        null=True,
        verbose_name=_("link to the event"))
    qr_code = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("QR code")
    )
    # todo padaryti protected
    qr_code_file = models.ImageField(
        verbose_name=_("QR code file"),
        upload_to="qrcodesimages",
        blank=True,
        null=True
    )
