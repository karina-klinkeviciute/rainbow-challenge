from django.db import models
from django.utils.translation import gettext_lazy as _

from joined_challenge.models import BaseJoinedChallenge


class StoryJoinedChallenge(BaseJoinedChallenge):

    story_url = models.URLField(
        verbose_name=_('link to the story if it has one'),
        blank=True,
        null=True
    )
    description = models.TextField(
        verbose_name=_('description of your story'),
        blank=True,
        null=True
    )

    @property
    def concrete_challenge(self):
        from challenge.models import StoryChallenge
        return StoryChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)
