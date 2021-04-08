import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Prize(models.Model):
    """Model for prizes that are given for points (rainbows)"""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False)
    name = models.CharField(max_length=1000, verbose_name=_('name'))
    description = models.TextField(
        verbose_name=_('description'),
        null=True,
        blank=True
    )
    price = models.IntegerField(verbose_name=_('price'))
    amount = models.IntegerField(verbose_name=_('amount'))
