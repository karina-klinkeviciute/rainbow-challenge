from django.db import models
import uuid


class Region(models.Model):
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False)
