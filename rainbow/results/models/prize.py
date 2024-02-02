import uuid
from datetime import datetime

from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from results.utils import message_site_admins


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
    image = models.ImageField(verbose_name=_('image'), upload_to='prize', blank=True, null=True)
    available = models.BooleanField(verbose_name=_('available'), default=True)
    expires_at = models.DateField(verbose_name=_('expiration date'), blank=True, null=True)

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
        'results.Prize',
        verbose_name=_('prize'),
        on_delete=models.CASCADE,
    )
    notes = models.TextField(verbose_name=_('notes'), blank=True, null=True)
    amount = models.IntegerField(verbose_name=_('amount'))
    issued = models.BooleanField(verbose_name=_('issued'), default=False)
    date_claimed = models.DateTimeField(verbose_name=_("date claimed"), auto_now_add=True)
    date_issued = models.DateTimeField(verbose_name=_("date issued"), blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if (self.issued is True) and (self.date_issued is None):
            self.date_issued = datetime.now()
            # self.galiojimo_pabaiga = self.pateikimo_data
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        if self.issued is False:
            message_site_admins(
                _("Prize confirmation needed"),
                _("User has just claimed a prize. Please issue it.")
            )
