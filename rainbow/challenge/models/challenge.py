import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.apps import apps

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

    CLASSES = {
        ARTICLE: 'ArticleChallenge',
        EVENT: 'EventParticipantChallenge',
    }


class Challenge(models.Model):
    """
    Model for common information on challenges. It will help calculations of points, statistics, search.
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    type = models.CharField(
        max_length=50,
        choices=ChallengeType.TYPE_CHOICES,
        verbose_name=_("type")
    )
    name = models.CharField(max_length=255, verbose_name=_("name"))
    description = models.TextField(verbose_name=_("description"))
    published = models.BooleanField(verbose_name=_('is published'), default=False)
    points = models.IntegerField(verbose_name=_("points"))
    region = models.ForeignKey(
        'challenge.Region',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("region")
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('start date')
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('end_date')
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

    @property
    def concrete_challenge_uuid(self):
        """
        Information that we have about a specific challenge
        """
        challenge_class = ChallengeType.CLASSES[self.type]
        model = apps.get_model('challenge', challenge_class)
        info = model.objects.get(main_challenge=self)
        return info.uuid

    @property
    def challenge_model(self):
        challenge_class = ChallengeType.CLASSES[self.type]
        model = apps.get_model('challenge', challenge_class)
        return model

    def __str__(self):
        return f"{self.name} - type: {self.type}"


class BaseChallenge(models.Model):
    """Base class for other challenge models"""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    main_challenge = models.OneToOneField(
        Challenge,
        verbose_name=_("main challenge"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"concrete challenge for {self.main_challenge.name} - type: {self.main_challenge.type}"


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
