import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from challenge.models.challenge import ArticleChallenge, EventParticipantChallenge


class JoinedChallengeStatus:
    """Class for challenge types. Used in choices for Challenge Type"""
    JOINED = 'joined'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (JOINED, _('joined')),
        (COMPLETED, _('completed')),
        (CANCELLED, _('cancelled')),
    )


class JoinedChallenge(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False)
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
        max_length=255)

    def __str__(self):
        return f'{self.user.username} - {self.challenge.name}'


class BaseJoinedChallenge(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False)
    main_joined_challenge = models.OneToOneField(
        'challenge.JoinedChallenge',
        verbose_name=_('main joined challenge'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    class Meta:
        abstract = True


class ArticleJoinedChallenge(BaseJoinedChallenge):
    article_name = models.TextField(verbose_name=_("name of the article"))
    article_url = models.TextField(verbose_name=_('link to the article'))

    @property
    def article_challenge(self):
        return ArticleChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)


class EventParticipantJoinedChallenge(BaseJoinedChallenge):

    @property
    def article_challenge(self):
        return EventParticipantChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)
