import uuid
import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from private_storage.fields import PrivateFileField


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
        if self.completed_at is None and (
                self.status == JoinedChallengeStatus.COMPLETED
                or self.status == JoinedChallengeStatus.CONFIRMED):
            self.completed_at = datetime.datetime.now()
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    def __str__(self):
        return f'{self.user.email} - {self.challenge.name} / {self.challenge.type}'


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
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        text = _("concrete joined challenge for: ")
        return f" {text}{self.main_joined_challenge.__str__()}"

    @property
    def concrete_challenge(self):
        raise NotImplementedError






