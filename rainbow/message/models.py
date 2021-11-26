import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class MessageTypes:
    MEDAL = "medal"

    MessageChoices = (
        (MEDAL, _("medal")),
    )


class Message(models.Model):
    """
    Class for messages that are sent either automatically by an app or between users and admins.
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    message_text = models.TextField(
        verbose_name=_("message text"),
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        # get_user_model(),
        'user.User',
        verbose_name=_('user'),
        related_name="user_messages",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    admin_sender = models.ForeignKey(
        # get_user_model(),
        'user.User',
        verbose_name=_('admin__sender'),
        related_name="admin_messages",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    type = models.CharField(
        max_length=255,
        verbose_name=_("type"),
        choices=MessageTypes.MessageChoices,
        blank=True,
        null=True
    )
    automated = models.BooleanField(
        verbose_name=_("automated"),
        default=True
    )
    time_sent = models.DateTimeField(
        verbose_name=_("time of sending"),
        auto_now_add=True
    )
    seen = models.BooleanField(
        verbose_name="seen",
        default=False
    )
    # there might be aneed to attach files.
    # In that case we need a new model "attachments" which would point to a message
