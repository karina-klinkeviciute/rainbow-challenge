import uuid
import datetime

from django.apps import apps
from django.db import models
from django.utils import translation
from django.utils.translation import gettext_lazy as _, gettext
from private_storage.fields import PrivateFileField

from challenge.models.base import ChallengeType
from message.models import Message, MessageTypes


class JoinedChallengeStatus:
    """Class for challenge types. Used in choices for Challenge Type"""
    JOINED = 'joined'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    CONFIRMED = 'confirmed'

    STATUS_CHOICES = (
        (JOINED, _('joined')),
        (COMPLETED, _('completed')),
        (CANCELLED, _('cancelled')),
        (CONFIRMED, _('confirmed')),
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
        null=True, blank=True, )
    status = models.CharField(
        verbose_name=_('status'),
        choices=JoinedChallengeStatus.STATUS_CHOICES,
        max_length=255,
        default=JoinedChallengeStatus.JOINED
    )
    joined_at = models.DateTimeField(
        verbose_name=_('joined at'),
        auto_now_add=True,
        null=True, blank=True
    )
    completed_at = models.DateTimeField(
        verbose_name=_('completed at'),
        null=True, blank=True
    )

    @property
    def files(self):
        return self.joinedchallengefile_set

    def files_admin(self):
        """property to return a list of files in a convenient enough format for admin"""
        files = self.joinedchallengefile_set
        file_list = []
        for file in files:
            file_list.append(file.file)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """Overridden save method for the model"""

        # adding completed_at if challenge is completed (or confirmed which in some use cases skips step 'completed')
        if self.completed_at is None and (
                self.status == JoinedChallengeStatus.COMPLETED
                or self.status == JoinedChallengeStatus.CONFIRMED):
            self.completed_at = datetime.datetime.now()
            # Also this means that we need to add 1 streak if this is the first challenge in the week.
            from results.utils import update_streak
            update_streak(self.user)

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        # Sending a notification about confirmation of the challenge
        if self.status == JoinedChallengeStatus.CONFIRMED:

            # Points for quiz are calculated based on the amount of correct answers
            if self.challenge_type == ChallengeType.QUIZ:
                points = self.quizjoinedchallenge.correct_answers_count
            else:
                points = self.challenge.points
            # todo make translation work
            message_text = gettext(
                "Užduoties atlikimas patvirtintas užduočiai: "
            ) + self. challenge.name + gettext(
                ". Sveikinam! "
            ) + gettext(" Gavai taškų: ") + str(points)
            print(message_text)
            message = Message(message_text=message_text, user=self.user, type=MessageTypes.CHALLENGE_CONFIRMATION)
            message.save()

    def __str__(self):
        return f'{self.user.email} - {self.challenge.name} / {self.challenge.type}'

    @property
    def concrete_joined_challenge(self):
        """
        Information that we have about a specific challenge
        """
        joined_challenge_class = ChallengeType.JOINED_CHALLENGE_CLASSES[self.challenge.type]
        model = apps.get_model('joined_challenge', joined_challenge_class)
        info = model.objects.get(main_joined_challenge=self)
        return info.uuid

    @property
    def challenge_type(self):
        return self.challenge.type

    @property
    def final_points(self):
        if self.challenge_type == ChallengeType.QUIZ:
            points = self.quizjoinedchallenge.correct_answers_count
        else:
            points = self.challenge.points
        return points


def upload_subfolder(instance):
    return [str(instance.joined_challenge.user.uid)]


class JoinedChallengeFile(models.Model):
    """
    Class for files to upload to joined challenges. All sorts of files, usually uploaded as proofs of completion.
    """
    joined_challenge = models.ForeignKey(
        JoinedChallenge,
        verbose_name=_("joined challenge"),
        on_delete=models.CASCADE,
    )
    file = PrivateFileField(
        verbose_name=_("file"),
        upload_to="joined_challenge_files",
        upload_subfolder=upload_subfolder
    )
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )


class BaseJoinedChallenge(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        primary_key=True,
        editable=False)
    main_joined_challenge = models.OneToOneField(
        'joined_challenge.JoinedChallenge',
        verbose_name=_('main joined challenge'),
        on_delete=models.CASCADE,
        null=True,
        blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        text = _("concrete joined challenge for: ")
        return f" {text}{self.main_joined_challenge.__str__()}"
