import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Text(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    body = models.TextField(verbose_name=_("body"))
    title = models.CharField(verbose_name=_("title"), max_length=255)
    notes = models.TextField(verbose_name=_("notes"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
