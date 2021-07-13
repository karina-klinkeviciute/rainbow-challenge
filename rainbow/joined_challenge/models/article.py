from django.db import models
from django.utils.translation import gettext_lazy as _

from joined_challenge.models.base import BaseJoinedChallenge


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
    def concrete_challenge(self):
        from challenge.models import ArticleChallenge
        return ArticleChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)
