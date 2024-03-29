from django.db import models
from django.utils.translation import gettext_lazy as _

from challenge.models.base import BaseChallenge


class SupportChallenge(BaseChallenge):
    """Support challenge"""
    organization = models.CharField(
        verbose_name=_('organization'),
        max_length=1000,
        null=True,
        blank=True
    )
