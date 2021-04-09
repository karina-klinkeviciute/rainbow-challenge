import uuid

from django.db import models
from django.db.models import Sum
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

    def __str__(self):
        return self.name

    @property
    def amount_remaining(self):
        amount_used = self.claimedprize_set.aggregate(Sum('amount'))['amount__sum']
        if amount_used is None:
            amount_used = 0
        remaining = self.amount - amount_used
        return remaining
#     todo write tests for this


class ClaimedPrize(models.Model):
    """
    Model to store who claimed what prize for how many points
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False)
    user = models.ForeignKey(
        'user.User',
        verbose_name=_('user'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    prize = models.ForeignKey(
        Prize,
        verbose_name=_('prize'),
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(verbose_name=_('amount'))
    issued = models.BooleanField(verbose_name=_('issued'), default=False)
