import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Message(models.Model):
    """
    Class for messages that are sent either automatically by an app or between users and admins.
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    ),
    message_text = models.TextField(
        verbose_name=_("message text")
    ),
    user = models.ForeignKey(
        # get_user_model(),
        'user.User',
        verbose_name=_('user'),
        on_delete=models.CASCADE),
    admin_sender = models.ForeignKey(
        # get_user_model(),
        'user.User',
        verbose_name=_('admin_sender'),
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    ),
    automatic = models.BooleanField(
        verbose_name=_("automatic"),
        default=True
    )
    time_sent = models.DateTimeField(
        verbose_name=_("time of sending"),
        auto_now_add=True
    )
    # there might be aneed to attach files.
    # In that case we need a new model "attachments" which would point to a message
