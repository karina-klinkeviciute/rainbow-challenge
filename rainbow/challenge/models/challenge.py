import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class ChallengeType:
    """Class for challenge types. Used in choices for Challenge Type"""
    QUIZ = 'quiz'
    ARTICLE = 'article'
    EVENT = 'event'
    CUSTOM = 'custom'

    TYPE_CHOICES = (
        (QUIZ, _('quiz')),
        (ARTICLE, _('article')),
        (EVENT, _('event')),
        (CUSTOM, _('custom'))
    )


class Challenge(models.Model):
    """
    Model for common information on callenges. It will help calculations of points, statistics, search.
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"))
    points = models.IntegerField(verbose_name=_("points"))
    type = models.CharField(
        max_length=50,
        choices=ChallengeType.TYPE_CHOICES,
        verbose_name=_("type")
    )
    multiple = models.BooleanField(
        help_text=_("can the participant join this challenge more than once"),
        verbose_name=_("multiple")
    )
    needs_confirmation = models.BooleanField(
        help_text=_("if completion of this challenge needs to be confirmed by admins"),
        verbose_name=_("required confirmation by admin")
    )
#     data for separate challenge types will be saved
#     in other models which will have a foreign key to this model
#     I think this is better than extending this class,
#     because in some cases only the general data will be enough
#     so it is useful to have one class for all tasks

    def __str__(self):
        return self.name


class BaseChallenge(models.Model):
    """Base class for other challenge models"""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False)
    main_challenge = models.ForeignKey(
        Challenge,
        verbose_name=_("main challenge"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    class Meta:
        abstract = True


class ArticleChallenge(BaseChallenge):
    """Article challenge"""
    pass


class EventParticipantChallenge(BaseChallenge):
    """Event participant challenge is when you
    participate in some event organized by others"""
    event_name = models.CharField(
        max_length=1000,
        verbose_name=_("event name")
    )
    region = models.ForeignKey(
        'challenge.Region',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("region")
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
