import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class JoinedChallengeStatus:
    """Class for challenge types. Used in choices for Challenge Type"""
    JOINED = 'joined'
    COMPLETED = 'completed'
    PENDING = 'pending'  # waiting for confirmation
    CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (JOINED, _('joined')),
        (COMPLETED, _('completed')),
        (PENDING, _('pending')),  # waiting for confirmation
        (CANCELLED, _('cancelled')),
    )


class JoinedChallenge(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    user = models.ForeignKey(
        # get_user_model(),
        'user.User',
        verbose_name=_('user'),
        on_delete=models.SET_NULL,
        null=True)
    challenge = models.ForeignKey(
        'challenge.Challenge',
        verbose_name=_('challenge'),
        on_delete=models.SET_NULL,
        null=True, blank=True)
    status = models.CharField(
        verbose_name=_('status'),
        choices=JoinedChallengeStatus.STATUS_CHOICES,
        max_length=255,
        default=JoinedChallengeStatus.JOINED
    )

    def __str__(self):
        return f'{self.user.username} - {self.challenge.name} / {self.challenge.type}'


class BaseJoinedChallenge(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False)
    main_joined_challenge = models.OneToOneField(
        'challenge.JoinedChallenge',
        verbose_name=_('main joined challenge'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"concrete challenge for {self.main_joined_challenge.__str__()}"

    @property
    def concrete_challenge(self):
        raise NotImplementedError