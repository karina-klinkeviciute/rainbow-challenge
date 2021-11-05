import uuid
from django.db import models


class NewsItem(models.Model):
    """News model. Returns latest news entered by admins"""
    title = models.CharField(max_length=1000)
    body = models.TextField()
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
