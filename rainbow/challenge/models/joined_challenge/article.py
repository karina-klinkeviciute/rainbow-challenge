from django.db import models
from django.utils.translation import gettext_lazy as _

from challenge.models import ArticleChallenge
from challenge.models.joined_challenge.base import BaseJoinedChallenge


class ArticleJoinedChallenge(BaseJoinedChallenge):
    article_name = models.TextField(
        verbose_name=_("name of the article"),
        blank=True,
        null=True
    )
    article_url = models.URLField(
        verbose_name=_('link to the article'),
        blank=True,
        null=True
    )

    @property
    def article_challenge(self):
        return ArticleChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)
